import json
import logging
import requests
from flask import current_app

logger = logging.getLogger(__name__)

# =====================================================
# PROMPTS
# =====================================================

PATIENT_PROMPT = """
You are a clinical medical assistant for patients.

Symptoms:
{input}

Return ONLY valid JSON with this exact structure. If no laboratory or imaging tests are specifically required, explain that in the recommendations or return "Monitoring and rest" instead of an empty list to reassure the patient:
{{
  "conditions": [
    {{"name": "Condition name", "probability": 70}}
  ],
  "investigations": {{
    "tests": ["Routine check for fever", "..."],
    "imaging": ["None required for current symptoms", "..."]
  }},
  "specialist": {{
    "name": "Specialist name",
    "keyword": "search keyword"
  }},
  "severity": "mild | moderate | severe",
  "recommendations": ["Result summary", "..."]
}}
"""

DOCTOR_PROMPT = """
You are a clinical decision support AI for doctors.

Case:
{input}

Return ONLY valid JSON:
{{
  "probable_diagnosis": [
    {{"name": "Disease", "probability": 80}}
  ],
  "medications": [
    {{
      "name": "Drug",
      "dosage": "500 mg",
      "frequency": "Every 8 hours",
      "duration": "7 days"
    }}
  ],
  "required_tests": [],
  "notes": ""
}}
"""

PHARMACIST_PROMPT = """
You are a pharmaceutical assistant.

Drug query:
{input}

Return ONLY valid JSON:
{{
  "drug": "",
  "active_ingredient": "",
  "alternatives": [
    {{"name": "Alternative", "strength": "500 mg"}}
  ],
  "dosage": "",
  "contraindications": []
}}
"""

# =====================================================
# CORE LLM CALL
# =====================================================

def call_llm(prompt):
    try:
        payload = {
            "model": current_app.config["LLM_MODEL"],
            "messages": [
                {"role": "system", "content": "Return valid JSON ONLY. Use the exact keys provided in the template."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        r = requests.post(
            current_app.config["LLM_API_URL"],
            json=payload,
            timeout=current_app.config.get("LLM_TIMEOUT", 600)
        )
        r.raise_for_status()
        
        content = r.json()["choices"][0]["message"]["content"]
        
        # Robust JSON cleaning
        content = content.replace('```json', '').replace('```', '').strip()
        start = content.find('{')
        end = content.rfind('}')
        if start != -1 and end != -1:
            content = content[start:end+1]
            
        parsed = json.loads(content)
        
        # Schema Flexibility Patching
        # 1. Handle "probabilities" vs "conditions"
        if "probabilities" in parsed and "conditions" not in parsed:
            parsed["conditions"] = []
            for item in parsed["probabilities"]:
                # Normalize probability key
                prob_val = item.get("probability") or item.get("prob") or 50
                parsed["conditions"].append({"name": item.get("name", "Unknown"), "probability": prob_val})
        
        # 2. Handle flat investigations
        if "investigations" not in parsed:
            parsed["investigations"] = {
                "tests": parsed.get("tests", []),
                "imaging": parsed.get("imaging", [])
            }
            
        return parsed
        
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        # Return structured fallback for patient analysis
        return {
            "conditions": [
                {"name": "⚠️ Connectivity Issue / مشكلة في الاتصال: The analysis engine is currently busy or unreachable. Please verify LM Studio is running. / محرك التحليل مشغول حالياً أو لا يمكن الوصول إليه. يرجى التأكد من تشغيل LM Studio.", "probability": 0}
            ],
            "investigations": {
                "tests": [],
                "imaging": []
            },
            "specialist": {
                "name": "General Practitioner / طبيب عام",
                "keyword": "general practitioner"
            },
            "severity": "mild",
            "recommendations": [
                "1. Ensure LM Studio is active and the model is loaded. / تأكد من تشغيل LM Studio وتحميل الموديل.",
                "2. Check if your hardware is running slow due to large models. / تحقق مما إذا كان جهازك يعمل ببطء بسبب حجم الموديل.",
                "3. Try providing more specific symptoms for better results. / حاول تقديم أعراض أكثر تحديداً للحصول على نتائج أفضل."
            ]
        }

# =====================================================
# GOOGLE MAPS (Nearest Doctor)
# =====================================================

def find_nearest_doctor(lat, lng, keyword):
    key = current_app.config.get("GOOGLE_PLACES_KEY")
    if not key:
        return None

    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lng}&rankby=distance&keyword={keyword}&key={key}"
    )

    try:
        r = requests.get(url, timeout=10).json()
        if not r.get("results"):
            return None

        place = r["results"][0]
        return {
            "name": place.get("name"),
            "address": place.get("vicinity"),
            "map_url": f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}"
        }
    except Exception as e:
        logger.error(f"Maps Error: {e}")
        return None

# =====================================================
# AIService Class (Compatibility Wrapper)
# =====================================================

class AIService:
    @staticmethod
    def generate_response(system_prompt, user_input):
        """Maintains backward compatibility for DoctorAgent and PharmacistAgent."""
        full_prompt = f"{system_prompt}\n\nInput: {user_input}"
        try:
            payload = {
                "model": current_app.config["LLM_MODEL"],
                "messages": [
                    {"role": "system", "content": "You are a helpful medical assistant."},
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0.5
            }

            r = requests.post(
                current_app.config["LLM_API_URL"],
                json=payload,
                timeout=current_app.config.get("LLM_TIMEOUT", 120)
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"AIService.generate_response error: {e}")
            return "Sorry, I am unable to process your request at the moment due to a connection issue with the AI service."

    @staticmethod
    def call_llm(prompt):
        return call_llm(prompt)

    @staticmethod
    def find_nearest_doctor(lat, lng, keyword):
        return find_nearest_doctor(lat, lng, keyword)
