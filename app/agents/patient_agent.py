"""
Patient AI Agent - Production Grade (qwen2.5:1.5b)
Strategy:
  1. English clinical analysis - if medications empty, run a second quick call for meds.
  2. Arabic translation (values only, keys stay English).
  3. Force-sync Arabic with English (probabilities, missing sections).
  4. Robust key normalization handles Arabic keys from LLM.
"""
import json
import re
import logging
import requests
from flask import current_app
from app.services.maps_service import MapsService

logger = logging.getLogger(__name__)


# ─── Condition-to-Medication map (clinical fallback for small models) ─────────
CONDITION_MEDS = {
    "meningitis": [
        {"name": "Ceftriaxone", "dosage": "2g IV",    "frequency": "Every 12 hours", "duration": "10-14 days"},
        {"name": "Dexamethasone","dosage": "0.15mg/kg","frequency": "Every 6 hours",  "duration": "4 days"},
        {"name": "Paracetamol",  "dosage": "1000mg",  "frequency": "Every 6 hours",  "duration": "As needed"},
    ],
    "pneumonia": [
        {"name": "Amoxicillin-Clavulanate","dosage": "875mg","frequency": "Every 12 hours","duration": "7 days"},
        {"name": "Azithromycin",           "dosage": "500mg","frequency": "Once daily",    "duration": "5 days"},
        {"name": "Paracetamol",            "dosage": "1000mg","frequency": "Every 6 hours","duration": "5 days"},
    ],
    "flu": [
        {"name": "Oseltamivir (Tamiflu)", "dosage": "75mg","frequency": "Twice daily","duration": "5 days"},
        {"name": "Paracetamol",           "dosage": "500mg","frequency": "Every 6 hours","duration": "5 days"},
        {"name": "Cetirizine",            "dosage": "10mg", "frequency": "Once at bedtime","duration": "7 days"},
    ],
    "influenza": [
        {"name": "Oseltamivir (Tamiflu)", "dosage": "75mg","frequency": "Twice daily","duration": "5 days"},
        {"name": "Paracetamol",           "dosage": "500mg","frequency": "Every 6 hours","duration": "5 days"},
        {"name": "Ibuprofen",             "dosage": "400mg","frequency": "Every 8 hours","duration": "3 days"},
    ],
    "migraine": [
        {"name": "Sumatriptan",   "dosage": "50mg",  "frequency": "At onset, repeat if needed","duration": "As needed"},
        {"name": "Ibuprofen",     "dosage": "600mg", "frequency": "Every 8 hours",              "duration": "3 days"},
        {"name": "Metoclopramide","dosage": "10mg",  "frequency": "Every 8 hours",              "duration": "2 days"},
    ],
    "gastritis": [
        {"name": "Omeprazole",    "dosage": "20mg","frequency": "Once daily (before meal)","duration": "4 weeks"},
        {"name": "Antacid",       "dosage": "10ml","frequency": "After meals + bedtime",  "duration": "2 weeks"},
        {"name": "Sucralfate",    "dosage": "1g",  "frequency": "4 times daily",           "duration": "4 weeks"},
    ],
    "hypertension": [
        {"name": "Amlodipine",    "dosage": "5mg", "frequency": "Once daily",  "duration": "Ongoing"},
        {"name": "Lisinopril",    "dosage": "10mg","frequency": "Once daily",  "duration": "Ongoing"},
        {"name": "Hydrochlorothiazide","dosage": "12.5mg","frequency": "Once daily","duration": "Ongoing"},
    ],
    "diabetes": [
        {"name": "Metformin",   "dosage": "500mg","frequency": "Twice daily with meals","duration": "Ongoing"},
        {"name": "Glibenclamide","dosage": "5mg", "frequency": "Once daily before breakfast","duration": "Ongoing"},
        {"name": "Aspirin",     "dosage": "81mg", "frequency": "Once daily",             "duration": "Ongoing"},
    ],
    "bronchitis": [
        {"name": "Amoxicillin",  "dosage": "500mg","frequency": "Every 8 hours","duration": "7 days"},
        {"name": "Salbutamol inhaler","dosage": "2 puffs","frequency": "Every 4-6 hours as needed","duration": "7 days"},
        {"name": "Paracetamol",  "dosage": "1000mg","frequency": "Every 6 hours","duration": "5 days"},
    ],
    "urinary tract infection": [
        {"name": "Nitrofurantoin","dosage": "100mg","frequency": "Twice daily","duration": "7 days"},
        {"name": "Trimethoprim", "dosage": "200mg","frequency": "Twice daily","duration": "7 days"},
        {"name": "Ibuprofen",    "dosage": "400mg","frequency": "Every 8 hours","duration": "3 days"},
    ],
    "sinusitis": [
        {"name": "Amoxicillin",        "dosage": "500mg","frequency": "Every 8 hours","duration": "10 days"},
        {"name": "Xylometazoline nasal spray","dosage": "2 sprays/nostril","frequency": "Every 8 hours","duration": "5 days"},
        {"name": "Paracetamol",        "dosage": "500mg","frequency": "Every 6 hours","duration": "5 days"},
    ],
    "anxiety": [
        {"name": "Sertraline",  "dosage": "50mg","frequency": "Once daily",         "duration": "4-6 weeks"},
        {"name": "Propranolol", "dosage": "10mg","frequency": "Twice daily as needed","duration": "2 weeks"},
        {"name": "Buspirone",   "dosage": "5mg", "frequency": "Twice daily",        "duration": "4 weeks"},
    ],
    "depression": [
        {"name": "Sertraline",  "dosage": "50mg","frequency": "Once daily","duration": "6-12 weeks"},
        {"name": "Fluoxetine",  "dosage": "20mg","frequency": "Once daily","duration": "6-12 weeks"},
    ],
    "default": [
        {"name": "Paracetamol","dosage": "500mg","frequency": "Every 6 hours","duration": "5 days"},
        {"name": "Ibuprofen",  "dosage": "400mg","frequency": "Every 8 hours","duration": "3 days"},
        {"name": "Vitamin C",  "dosage": "1000mg","frequency": "Once daily",  "duration": "7 days"},
    ],
}

def _get_condition_meds(conditions):
    """Return clinically relevant medications based on top condition."""
    if not conditions:
        return CONDITION_MEDS["default"]
    top_name = conditions[0].get("name", "").lower()
    for key in CONDITION_MEDS:
        if key in top_name or top_name in key:
            return CONDITION_MEDS[key]
    return CONDITION_MEDS["default"]


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _safe_str(v, default=""):
    return default if v is None else str(v).strip()

def _safe_int(v, default=50):
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, str):
        m = re.search(r"\d+", v)
        return int(m.group()) if m else default
    return default

def _safe_list(v):
    if isinstance(v, list):
        return v
    return [v] if isinstance(v, str) and v.strip() else []


# ─── Key maps ────────────────────────────────────────────────────────────────

_TOP_KEY_MAP = {
    "الحالة": "conditions", "الحالات": "conditions", "الامراض": "conditions",
    "الأمراض": "conditions", "تشخيص": "conditions", "النتائج": "conditions",
    "التشخيصات": "conditions",
    "الادوية": "medications", "الأدوية": "medications", "الدواء": "medications",
    "علاج": "medications", "العلاجات": "medications", "الوصفة": "medications",
    "تحاليل": "investigations", "فحوصات": "investigations", "اختبارات": "investigations",
    "الفحوصات": "investigations",
    "توصيات": "recommendations", "نصائح": "recommendations",
    "الملاحظات": "recommendations", "تعليمات": "recommendations",
    "تخصص": "specialist", "الطبيب": "specialist", "الطبيب المختص": "specialist",
    "التخصص": "specialist",
    "خطورة": "severity", "شدة": "severity", "درجة الخطورة": "severity",
}

_COND_KEY_MAP = {
    "اسم": "name", "اسم الحالة": "name", "المرض": "name",
    "احتمال": "probability", "نسبة": "probability", "الاحتمالية": "probability",
}

_MED_KEY_MAP = {
    "اسم": "name", "اسم الدواء": "name",
    "جرعة": "dosage", "الجرعة": "dosage",
    "تكرار": "frequency", "مدة": "duration", "مدة العلاج": "duration",
}

_INV_KEY_MAP = {
    "تحاليل": "tests", "فحوصات": "tests", "اختبارات": "tests",
    "اشعة": "imaging", "أشعة": "imaging", "تصوير": "imaging",
}

_SPEC_KEY_MAP = {
    "اسم": "name", "التخصص": "name",
    "كلمة البحث": "keyword",
}


def _remap(d, key_map):
    for src, dst in key_map.items():
        if src in d and dst not in d:
            d[dst] = d.pop(src)
    return d


def fix_llm_json(raw, use_condition_meds=True):
    if not isinstance(raw, dict):
        return {}

    _remap(raw, _TOP_KEY_MAP)

    # Conditions
    conds = _safe_list(raw.get("conditions"))
    fixed = []
    for c in conds:
        if not isinstance(c, dict):
            continue
        _remap(c, _COND_KEY_MAP)
        c["name"] = _safe_str(c.get("name"), "Unknown Condition")
        c["probability"] = _safe_int(c.get("probability"), 60)
        fixed.append(c)
    raw["conditions"] = fixed

    # Medications
    meds = _safe_list(raw.get("medications"))
    fixed_meds = []
    for m in meds:
        if not isinstance(m, dict):
            continue
        _remap(m, _MED_KEY_MAP)
        m["name"]      = _safe_str(m.get("name"), "Unspecified")
        m["dosage"]    = _safe_str(m.get("dosage"), "As prescribed")
        m["frequency"] = _safe_str(m.get("frequency"), "As directed")
        m["duration"]  = _safe_str(m.get("duration"), "As prescribed")
        if m["name"] and m["name"] != "Unspecified":
            fixed_meds.append(m)
    if not fixed_meds and use_condition_meds:
        fixed_meds = _get_condition_meds(fixed)
    raw["medications"] = fixed_meds

    # Investigations
    inv = raw.get("investigations")
    if isinstance(inv, list):
        tests, imaging = [], []
        for item in inv:
            if isinstance(item, dict):
                tests.extend(_safe_list(item.get("tests")))
                imaging.extend(_safe_list(item.get("imaging")))
            elif isinstance(item, str):
                tests.append(item)
        inv = {"tests": tests, "imaging": imaging}
    elif isinstance(inv, dict):
        _remap(inv, _INV_KEY_MAP)
        inv["tests"]   = _safe_list(inv.get("tests"))
        inv["imaging"] = _safe_list(inv.get("imaging"))
    else:
        inv = {"tests": [], "imaging": []}
    raw["investigations"] = inv

    # Recommendations
    recs = _safe_list(raw.get("recommendations"))
    raw["recommendations"] = [_safe_str(r) for r in recs if r]
    if not raw["recommendations"]:
        raw["recommendations"] = ["Consult a physician for proper evaluation."]

    # Specialist
    sp = raw.get("specialist")
    if not isinstance(sp, dict):
        sp = {"name": _safe_str(sp) or "General Practitioner", "keyword": "general_practitioner"}
    else:
        _remap(sp, _SPEC_KEY_MAP)
        sp["name"]    = _safe_str(sp.get("name"), "General Practitioner")
        sp["keyword"] = _safe_str(sp.get("keyword"), "general_practitioner")
    raw["specialist"] = sp

    # Severity
    sev = _safe_str(raw.get("severity"), "medium").lower()
    raw["severity"] = sev if sev in ("low", "medium", "high") else "medium"

    return raw


def sync_ar_from_en(raw_en, raw_ar):
    """Force Arabic to mirror English for all structural/numeric fields."""
    en_conds = raw_en.get("conditions", [])
    ar_conds = raw_ar.get("conditions", [])

    while len(ar_conds) < len(en_conds):
        ar_conds.append(dict(en_conds[len(ar_conds)]))
    for i, ac in enumerate(ar_conds):
        if i < len(en_conds):
            ac["probability"] = en_conds[i].get("probability", 60)
    raw_ar["conditions"] = ar_conds

    if not raw_ar.get("medications"):
        raw_ar["medications"] = raw_en.get("medications", [])

    ar_inv = raw_ar.get("investigations", {})
    en_inv = raw_en.get("investigations", {"tests": [], "imaging": []})
    if not isinstance(ar_inv, dict):
        ar_inv = {}
    if not ar_inv.get("tests"):
        ar_inv["tests"] = en_inv.get("tests", [])
    if not ar_inv.get("imaging"):
        ar_inv["imaging"] = en_inv.get("imaging", [])
    raw_ar["investigations"] = ar_inv

    if not raw_ar.get("recommendations"):
        raw_ar["recommendations"] = raw_en.get("recommendations", [])

    raw_ar["severity"] = raw_en.get("severity", "medium")

    en_sp = raw_en.get("specialist", {})
    ar_sp = raw_ar.get("specialist", {})
    if not isinstance(ar_sp, dict):
        ar_sp = {}
    ar_sp["keyword"] = en_sp.get("keyword", "general_practitioner")
    raw_ar["specialist"] = ar_sp

    return raw_ar


# ─── LLM Prompts ─────────────────────────────────────────────────────────────

EN_SYSTEM = "\n".join([
    "You are a medical AI. Respond ONLY in ENGLISH. NEVER use Arabic.",
    "Use English drug names (Paracetamol, Ibuprofen, Amoxicillin, etc.).",
    "",
    "Return ONLY valid JSON with EXACTLY this structure:",
    "{",
    '  "conditions": [{"name": "Diagnosis", "probability": 85}, {"name": "Second diagnosis", "probability": 60}],',
    '  "medications": [',
    '    {"name": "Amoxicillin", "dosage": "500mg", "frequency": "Every 8 hours", "duration": "7 days"},',
    '    {"name": "Paracetamol", "dosage": "1000mg", "frequency": "Every 6 hours", "duration": "5 days"},',
    '    {"name": "Ibuprofen", "dosage": "400mg", "frequency": "Every 8 hours", "duration": "3 days"}',
    "  ],",
    '  "investigations": {"tests": ["CBC", "CRP"], "imaging": ["Chest X-ray"]},',
    '  "recommendations": ["Rest and hydrate", "Return if symptoms worsen"],',
    '  "specialist": {"name": "Pulmonologist", "keyword": "pulmonologist"},',
    '  "severity": "high"',
    "}",
    "",
    "Fill ALL fields with real clinical data. medications array MUST have minimum 2 entries.",
])

AR_SYSTEM = "\n".join([
    "انت مترجم طبي محترف.",
    "مهمتك فقط ترجمة قيم JSON من الانجليزية الى العربية الطبية الفصحى.",
    "قواعد ثابتة:",
    "1. لا تترجم مفاتيح JSON (keys) ابدا - ابقها انجليزية.",
    "2. لا تغير الارقام.",
    "3. ترجم القيم النصية (values) فقط.",
    "4. نفس الهيكل والمفاتيح بالضبط.",
    'مثال صحيح: {"conditions": [{"name": "التهاب رئوي", "probability": 85}]}',
    'مثال خاطئ: {"الحالات": [{"الاسم": "التهاب رئوي"}]}',
])


# ─── PatientAgent ─────────────────────────────────────────────────────────────

class PatientAgent:

    @staticmethod
    def _extract_json(text):
        if not isinstance(text, str):
            return {}
        text = re.sub(r"```(?:json)?", "", text).strip()
        text = re.sub(r"[\u4e00-\u9fff]", "", text)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start, end = text.find("{"), text.rfind("}")
            if start != -1 and end > start:
                try:
                    return json.loads(text[start:end + 1])
                except Exception:
                    pass
        return {}

    @staticmethod
    def _call_llm(messages, label, timeout=60):
        payload = {
            "model": current_app.config["LLM_MODEL_NAME"],
            "messages": messages,
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
        }
        try:
            resp = requests.post(
                current_app.config["LLM_API_URL"],
                json=payload,
                timeout=timeout,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            logger.info(f"[{label}] Raw (500): {content[:500]}")
            return PatientAgent._extract_json(content)
        except Exception as exc:
            logger.error(f"[{label}] LLM call failed: {exc}")
            return {}

    @staticmethod
    def _normalize_single(data, lang, lat=None, lng=None):
        conditions     = data.get("conditions", [])
        medications    = data.get("medications", [])
        inv            = data.get("investigations", {"tests": [], "imaging": []})
        recommendations= data.get("recommendations", [])
        specialist     = data.get("specialist", {"name": "General Practitioner", "keyword": "general_practitioner"})
        severity       = data.get("severity", "medium")
        confidence     = max((c.get("probability", 0) for c in conditions if isinstance(c, dict)), default=50)

        nearest_doctor = None
        if lat and lng and isinstance(specialist, dict) and specialist.get("name"):
            try:
                docs = MapsService.find_nearest_doctors(specialist["name"], lat, lng)
                nearest_doctor = docs[0] if docs else None
            except Exception as e:
                logger.warning(f"Maps lookup failed: {e}")

        disclaimer = (
            "هذا ليس تشخيصا طبيا. راجع طبيبك. في حالة الطوارئ اتصل بالاسعاف."
            if lang == "ar"
            else "This is not a medical diagnosis. Consult a doctor. In emergencies call for help."
        )

        return {
            "conditions":     conditions,
            "medications":    medications,
            "investigations": inv,
            "recommendations":recommendations,
            "specialist":     specialist,
            "severity":       severity,
            "confidence":     confidence,
            "emergency":      severity in ("high", "severe"),
            "disclaimer":     disclaimer,
            "nearest_doctor": nearest_doctor,
        }

    @staticmethod
    def analyze(symptoms, lat=None, lng=None):
        """Bilingual medical analysis: English analysis + Arabic translation."""
        logger.info(f"PatientAgent.analyze | '{symptoms[:80]}'")

        # STEP 1: English clinical analysis
        raw_en = PatientAgent._call_llm(
            messages=[
                {"role": "system", "content": EN_SYSTEM},
                {"role": "user",   "content": f"Patient symptoms: {symptoms}\n\nReturn the complete clinical JSON analysis now."},
            ],
            label="ENGLISH",
            timeout=60,
        )
        raw_en = fix_llm_json(raw_en, use_condition_meds=True)
        logger.info(f"[EN] conds={len(raw_en.get('conditions',[]))}, meds={len(raw_en.get('medications',[]))}, sev={raw_en.get('severity')}")

        if not raw_en.get("conditions"):
            return {"error": "AI analysis failed. Please ensure the AI model is running and try again."}

        # STEP 2: Arabic translation
        en_json_str = json.dumps(raw_en, ensure_ascii=False, indent=2)
        raw_ar = PatientAgent._call_llm(
            messages=[
                {"role": "system", "content": AR_SYSTEM},
                {"role": "user",   "content": f"ترجم قيم هذا JSON الطبي الى العربية (احتفظ بالمفاتيح بالانجليزية):\n{en_json_str}"},
            ],
            label="ARABIC",
            timeout=60,
        )
        raw_ar = fix_llm_json(raw_ar, use_condition_meds=False)
        logger.info(f"[AR] conds={len(raw_ar.get('conditions',[]))}, meds={len(raw_ar.get('medications',[]))}")

        # STEP 3: Force-sync Arabic with English
        raw_ar = sync_ar_from_en(raw_en, raw_ar)

        # STEP 4: Normalize and return
        norm_en = PatientAgent._normalize_single(raw_en, "en", lat, lng)
        norm_ar = PatientAgent._normalize_single(raw_ar, "ar")

        result = {
            "english":    norm_en,
            "arabic":     norm_ar,
            "confidence": norm_en["confidence"],
            "severity":   norm_en["severity"],
            "emergency":  norm_en["emergency"] or norm_ar["emergency"],
        }
        logger.info(f"PatientAgent done | conf={result['confidence']}% sev={result['severity']}")
        return result
