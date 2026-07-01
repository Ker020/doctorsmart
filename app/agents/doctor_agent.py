import json
import re
import logging
import requests
from flask import current_app

logger = logging.getLogger(__name__)

class DoctorAgent:
    """
    Professional clinical AI (Doctor only) - Provides advanced diagnostic support
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
        """Remove Chinese characters, punctuation and non-target scripts"""
        if not isinstance(text, str): return text
        # Remove Chinese range + Chinese punctuation/symbols
        pattern = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'
        return re.sub(pattern, '', text).strip()

    @staticmethod
    def normalize(raw):
        """Standardize the AI response for the clinical UI"""
        logger.info(f"Normalizing clinical raw data")
        
        def normalize_single(data):
            if not isinstance(data, dict): return {}
            
            # Clean conditions
            probs = data.get("conditions", [])
            if not isinstance(probs, list): probs = []
            for p in probs:
                if not isinstance(p, dict): continue
                p["name"] = DoctorAgent.clean_text(p.get("name", ""))
                # Handle prob as string or int
                p_val = p.get("prob")
                if isinstance(p_val, str):
                    try:
                        p_val = int(p_val.replace("%", ""))
                    except:
                        p_val = 50
                elif p_val is None:
                    p_val = 50
                p["prob"] = p_val

            # Clean medications
            meds = data.get("medications") or []
            if isinstance(meds, list):
                for m in meds:
                    if isinstance(m, dict):
                        m["name"] = DoctorAgent.clean_text(m.get("name", ""))
                        m["dosage"] = DoctorAgent.clean_text(m.get("dosage", ""))
                        m["duration"] = DoctorAgent.clean_text(m.get("duration", ""))
            else:
                meds = []

            # Clean investigations
            inv = data.get("investigations") or {}
            if not isinstance(inv, dict): inv = {}
            tests = [DoctorAgent.clean_text(t) for t in (inv.get("tests") or []) if isinstance(t, str)]
            imaging = [DoctorAgent.clean_text(t) for t in (inv.get("imaging") or []) if isinstance(t, str)]
            
            # Clean recommendations
            recs = [DoctorAgent.clean_text(r) for r in (data.get("recommendations") or []) if isinstance(r, str)]
            
            severity = str(data.get("severity", "medium")).lower()

            return {
                "probabilities": probs,
                "medications": meds,
                "tests": tests + imaging,
                "recommendations": recs,
                "severity": severity,
                "confidence": int(data.get("confidence", 70)) if str(data.get("confidence")).isdigit() else 70,
                "emergency": severity in ["high", "severe", "emergency", "طوارئ", "عالية"]
            }

        # Handle bilingual structure
        if "english" in raw and "arabic" in raw:
            norm_en = normalize_single(raw["english"])
            norm_ar = normalize_single(raw["arabic"])
            
            # Data Alignment & Fallback Logic
            if not norm_ar["medications"] and norm_en["medications"]:
                norm_ar["medications"] = norm_en["medications"]
            if not norm_ar["recommendations"] and norm_en["recommendations"]:
                norm_ar["recommendations"] = norm_en["recommendations"]
            if not norm_ar["probabilities"] and norm_en["probabilities"]:
                norm_ar["probabilities"] = norm_en["probabilities"]
            if not norm_ar["tests"] and norm_en["tests"]:
                norm_ar["tests"] = norm_en["tests"]
                
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
        system_msg = "You are a senior clinical consultant AI. Respond ONLY in valid JSON."
        if is_translation:
            system_msg = "You are a medical translator. Translate the provided clinical analysis into Arabic, keeping identical structure and probabilities."

        payload = {
            "model": current_app.config["LLM_MODEL_NAME"],
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,
            "max_tokens": 3000,
            "response_format": {"type": "json_object"}
        }
        try:
            url = current_app.config.get("LLM_API_URL") or current_app.config.get("LLM_URL")
            response = requests.post(url, json=payload, timeout=600)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            logger.debug(f"DoctorAgent [{language_name}] Raw Content: {content}")
            content = DoctorAgent.clean_text(content)
            return DoctorAgent.extract_json(content)
        except Exception as ex:
            logger.error(f"DoctorAgent [{language_name}] Call failed: {ex}")
            return None

    @staticmethod
    def fix_llm_json(raw):
        """Fix common LLM JSON mistakes and handle translated keys"""
        if not isinstance(raw, dict): return {}
        key_map = {
            "الحالة": "conditions", "الحالات": "conditions", "الامراض": "conditions", "تشخيص": "conditions",
            "الادوية": "medications", "الأدوية": "medications", "علاج": "medications",
            "تحاليل": "investigations", "فحوصات": "investigations", "اختبارات": "investigations", "التشخيص": "investigations",
            "توصيات": "recommendations", "نصائح": "recommendations", "الملاحظات": "recommendations",
            "خطورة": "severity", "شدة": "severity", "الخطر": "severity"
        }
        for k, v in list(raw.items()):
            if k in key_map:
                mapped_key = key_map[k]
                if mapped_key not in raw: raw[mapped_key] = raw.pop(k)

        conditions = raw.get("conditions", [])
        if not isinstance(conditions, list): conditions = []
        for c in conditions:
            if not isinstance(c, dict): continue
            if "اسم" in c: c["name"] = c.pop("اسم")
            if "احتمال" in c: c["prob"] = c.pop("احتمال")
            if "المخاطر" in c: c["prob"] = c.pop("المخاطر")
            
        meds = raw.get("medications", [])
        if isinstance(meds, list):
            for m in meds:
                if not isinstance(m, dict): continue
                if "اسم" in m: m["name"] = m.pop("اسم")
                if "جرعة" in m: m["dosage"] = m.pop("جرعة")
                if "تكرار" in m: m["frequency"] = m.pop("تكرار")
                if "مدة" in m: m["duration"] = m.pop("مدة")

        inv = raw.get("investigations", {})
        if isinstance(inv, dict):
            if "تحاليل" in inv: inv["tests"] = inv.pop("تحاليل")
            if "اشعة" in inv: inv["imaging"] = inv.pop("اشعة")
            if not isinstance(inv.get("tests"), list): inv["tests"] = []
            if not isinstance(inv.get("imaging"), list): inv["imaging"] = []
        raw["conditions"] = conditions
        return raw

    @staticmethod
    def analyze(clinical_input):
        """Main endpoint for professional diagnostic support (Total Isolation)"""
        
        # 1. Primary English Analysis
        en_prompt = f"""As a senior clinical consultant, perform a detailed diagnostic analysis for:
{clinical_input}

1. DIAGNOSIS: Provide at least 2-3 differential diagnoses with probabilities.
2. TREATMENT: Suggest specific medications (name, dose, duration) and detailed recommendations.
3. FOLLOW-UP: List necessary labs and imaging.
4. RICHNESS: Provide a professional, deep analysis without generic placeholders.

Return ONLY this JSON structure:
{{
  "conditions": [ {{"name": "Detailed Diagnosis", "prob": 80}} ],
  "medications": [ {{"name": "Medication Name", "dosage": "500mg", "duration": "5 days"}} ],
  "investigations": {{ "tests": ["Lab Test"], "imaging": ["Imaging Scan"] }},
  "recommendations": ["Detailed Clinical Advice"],
  "severity": "low/medium/high",
  "confidence": 85
}}"""

        logger.info(f"Starting clinical English analysis for: {clinical_input[:50]}...")
        raw_en = DoctorAgent._call_llm(en_prompt, "ENGLISH")
        raw_en = DoctorAgent.fix_llm_json(raw_en or {})
        
        if not raw_en:
            return {"error": "Clinical analysis failed. Please try again with more details."}

        # 2. Translation to Arabic
        ar_prompt = f"""Translate this professional clinical JSON report into ARABIC.
MANDATORY: 
1. The structure, probability percentages, and indices MUST remain identical.
2. Translate only the values (names, dosages, descriptions).
3. Use professional clinical Arabic terminology.

JSON to Translate:
{json.dumps(raw_en, ensure_ascii=False)}"""

        logger.info("Translating clinical analysis to Arabic...")
        raw_ar = DoctorAgent._call_llm(ar_prompt, "ARABIC_TRANSLATION", is_translation=True)
        raw_ar = DoctorAgent.fix_llm_json(raw_ar or {})

        merged = {
            "english": raw_en,
            "arabic": raw_ar if raw_ar else {}
        }

        return DoctorAgent.normalize(merged)

    @staticmethod
    def assist_diagnosis(symptoms, history="No history provided"):
        """Simple text-based advice for the patient view in doctor dashboard"""
        prompt = f"Symptoms: {symptoms}\nPatient History: {history}\n\nProvide a concise clinical summary and top 3 priorities for the doctor."
        
        payload = {
            "model": current_app.config["LLM_MODEL_NAME"],
            "messages": [
                {"role": "system", "content": "You are a professional medical consultant. Be brief and clinical."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }

        try:
            url = current_app.config.get("LLM_API_URL") or current_app.config.get("LLM_URL")
            response = requests.post(
                url,
                json=payload,
                timeout=600
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Quick assist failed: {e}")
            return "Unable to generate insights at this time."
