import json
import re
import logging
import requests
from flask import current_app

logger = logging.getLogger(__name__)

class PharmacistAgent:
    """
    Medication counseling ONLY – provides drug alternatives and dosage information
    """

    @staticmethod
    def extract_json(text):
        try:
            return json.loads(text)
        except:
            start, end = text.find("{"), text.rfind("}")
            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end+1])
                except:
                    return {}
        return {}

    @staticmethod
    def clean_text(text):
        """Remove Chinese characters, punctuation, and non-target scripts"""
        if not isinstance(text, str): return text
        # Remove Chinese range + Chinese punctuation/symbols
        pattern = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'
        return re.sub(pattern, '', text).strip()

    @staticmethod
    def normalize(raw):
        """Standardize pharmacist AI response with robust fallbacks"""
        logger.info(f"Normalizing pharmacist raw data")
        
        def normalize_single(data):
            if not isinstance(data, dict): return {}
            
            # Helper to extract text from list or string
            def get_text(val, default="N/A"):
                if isinstance(val, str): return val
                if isinstance(val, list):
                    items = []
                    for item in val:
                        if isinstance(item, str): items.append(item)
                        elif isinstance(item, dict):
                            name = item.get("name") or item.get("type") or ""
                            desc = item.get("amount") or item.get("description") or ""
                            items.append(f"{name} ({desc})" if name and desc else name or desc)
                    return " + ".join(filter(None, items))
                return default

            # Helper to extract list from list of strings or objects
            def get_list(val):
                if not isinstance(val, list): return []
                res = []
                for item in val:
                    if isinstance(item, str): res.append(PharmacistAgent.clean_text(item))
                    elif isinstance(item, dict):
                        name = item.get("name") or item.get("type") or ""
                        desc = item.get("warnings") or item.get("description") or ""
                        if isinstance(desc, list): desc = ", ".join(desc)
                        txt = f"{name}: {desc}" if name and desc else name or desc
                        res.append(PharmacistAgent.clean_text(txt))
                return res

            return {
                "active_ingredient": PharmacistAgent.clean_text(get_text(data.get("active_ingredient"), "N/A")),
                "dosage": PharmacistAgent.clean_text(data.get("dosage", "N/A")),
                "alternatives": [
                    {
                        "name": PharmacistAgent.clean_text(alt.get("name", "Unknown")),
                        "warnings": [PharmacistAgent.clean_text(w) for w in (alt.get("warnings") or []) if isinstance(w, str)]
                    } for alt in (data.get("alternatives") or []) if isinstance(alt, dict)
                ],
                "contraindications": get_list(data.get("contraindications")),
                "allergy_warnings": get_list(data.get("allergy_warnings")),
                "side_effects": get_list(data.get("side_effects"))
            }

        # Handle bilingual structure
        if "english" in raw and "arabic" in raw:
            norm_en = normalize_single(raw["english"])
            norm_ar = normalize_single(raw["arabic"])
            
            # Data Alignment & Fallback for Arabic
            if not norm_ar["active_ingredient"] or norm_ar["active_ingredient"] in ["N/A", "الاسم"]:
                norm_ar["active_ingredient"] = norm_en["active_ingredient"]
            
            if not norm_ar["dosage"] or norm_ar["dosage"] == "N/A":
                norm_ar["dosage"] = norm_en["dosage"]
            
            if not norm_ar["alternatives"] and norm_en["alternatives"]:
                norm_ar["alternatives"] = norm_en["alternatives"]
            if not norm_ar["contraindications"] and norm_en["contraindications"]:
                norm_ar["contraindications"] = norm_en["contraindications"]
            if not norm_ar["allergy_warnings"] and norm_en["allergy_warnings"]:
                norm_ar["allergy_warnings"] = norm_en["allergy_warnings"]
            if not norm_ar["side_effects"] and norm_en["side_effects"]:
                norm_ar["side_effects"] = norm_en["side_effects"]

            return {
                "english": norm_en,
                "arabic": norm_ar
            }
        else:
            # Fallback for flat response
            content_str = str(raw)
            is_arabic = any("\u0600" <= c <= "\u06FF" for c in content_str)
            norm = normalize_single(raw)
            return {
                "english": norm,
                "arabic": norm if is_arabic else {} 
            }

    @staticmethod
    def _call_llm(prompt, language_name, is_translation=False):
        system_msg = "You are a senior pharmaceutical clinical AI. Respond ONLY in valid JSON."
        if is_translation:
            system_msg = "You are a professional medical translator. Your task is to translate the following pharmaceutical JSON report into ARABIC. You MUST translate every description and value. Do NOT leave English text in the values. Return the same JSON structure."
        
        payload = {
            "model": current_app.config["LLM_MODEL_NAME"],
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,
            "max_tokens": 2000,
            "response_format": {"type": "json_object"}
        }
        try:
            url = current_app.config.get("LLM_API_URL") or current_app.config.get("LLM_URL")
            response = requests.post(url, json=payload, timeout=600)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            logger.debug(f"Pharmacist [{language_name}] Raw Content: {content}")
            content = PharmacistAgent.clean_text(content)
            return PharmacistAgent.extract_json(content)
        except Exception as ex:
            logger.error(f"Pharmacist [{language_name}] Call failed: {ex}")
            return None

    @staticmethod
    def fix_llm_json(raw):
        """Fix common LLM JSON mistakes and handle translated keys"""
        if not isinstance(raw, dict): return {}
        key_map = {
            "المادة الفعالة": "active_ingredient", "مكونات": "active_ingredient",
            "الجرعة": "dosage", "طريقة الاستخدام": "dosage",
            "البدائل": "alternatives", "بديل": "alternatives",
            "موانع الاستعمال": "contraindications", "تحذيرات": "contraindications",
            "الحساسية": "allergy_warnings", "تحذيرات الحساسية": "allergy_warnings",
            "الآثار الجانبية": "side_effects", "الاعراض الجانبية": "side_effects"
        }
        for k, v in list(raw.items()):
            if k in key_map:
                mapped_key = key_map[k]
                if mapped_key not in raw: raw[mapped_key] = raw.pop(k)

        alts = raw.get("alternatives", [])
        if isinstance(alts, list):
            for a in alts:
                if not isinstance(a, dict): continue
                if "اسم" in a: a["name"] = a.pop("اسم")
                if "تحذيرات" in a: a["warnings"] = a.pop("تحذيرات")
        return raw

    @staticmethod
    def analyze(drug_input):
        """Analyze medication using Total Isolation (EN -> AR Translation)"""
        
        # 1. Primary English Analysis - High Richness
        en_prompt = f"""As a senior clinical pharmacist, provide a COMPLETE pharmaceutical report for: {drug_input}

1. IDENTITY: If it's a brand (e.g., 'Pialcofan', 'Panadol', 'Congestal'), you MUST identify all active ingredients (e.g., 'Paracetamol 500mg, Caffeine 30mg'). Correct any spelling (e.g., 'parastaoml' -> 'Paracetamol').
2. DOSAGE: Provide precise typical adult dosages (e.g., '1-2 tablets every 6 hours, max 8 tabs/24h').
3. SAFETY: List ALL common contraindications, specific substance allergies, and both common/serious side effects.
4. RICHNESS: Do not use placeholders. Provide a detailed, professional analysis.

Return ONLY this JSON structure:
{{
  "active_ingredient": "Specific Chemical Name(s) and strength",
  "dosage": "Precise clinical dosage guidelines",
  "alternatives": [ {{ "name": "Generic or Brand Alternative", "warnings": ["Reason for caution"] }} ],
  "contraindications": ["List of conditions"],
  "allergy_warnings": ["Substances to avoid"],
  "side_effects": ["Detailed list of effects"]
}}"""

        logger.info(f"Starting pharmacist English analysis for: {drug_input}")
        raw_en = PharmacistAgent._call_llm(en_prompt, "ENGLISH")
        raw_en = PharmacistAgent.fix_llm_json(raw_en or {})
        
        if not raw_en:
            return {"error": "Failed to analyze medication. Please check spelling and try again."}

        # 2. Translation to Arabic
        ar_prompt = f"""Translate this specific clinical JSON report into pharmaceutical ARABIC. 
MANDATORY INSTRUCTIONS:
1. Keep the JSON structure IDENTICAL.
2. Translate ALL values (strings) to Arabic. 
3. DO NOT leave English descriptions. 
4. Use professional clinical Arabic terminology (e.g., 'Paracetamol' -> 'باراسيتامول').
5. Preserve numerical values exactly.

JSON to Translate:
{json.dumps(raw_en, ensure_ascii=False)}"""

        logger.info("Translating pharmaceutical analysis to Arabic...")
        raw_ar = PharmacistAgent._call_llm(ar_prompt, "ARABIC_TRANSLATION", is_translation=True)
        raw_ar = PharmacistAgent.fix_llm_json(raw_ar or {})

        merged = {
            "english": raw_en,
            "arabic": raw_ar if raw_ar else {}
        }

        return PharmacistAgent.normalize(merged)

    @staticmethod
    def suggest_alternatives(drug_name):
        """Wrapper to get just alternatives for the dashboard"""
        result = PharmacistAgent.analyze(drug_name)
        if "error" in result:
            return "No alternatives found."
        
        # safely extract english alternatives
        try:
            alts = result.get('english', {}).get('alternatives', [])
            if not alts:
                return "No known alternatives."
            
            # format as string
            return ", ".join([a['name'] for a in alts])
        except:
            return "Error parsing alternatives."
