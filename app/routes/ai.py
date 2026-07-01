from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import login_required
from app.agents.patient_agent import PatientAgent
from app.agents.doctor_agent import DoctorAgent
from app.utils.decorators import role_required

bp = Blueprint("ai", __name__, url_prefix="/ai")

@bp.route('/patient')
@login_required
def patient_ai():
    return render_template('patient/ai_assistant.html', google_maps_key=current_app.config.get("GOOGLE_MAPS_API_KEY"))

@bp.route('/doctor')
@login_required
def doctor_ai():
    return render_template('doctor/ai_assistant.html')

@bp.route('/pharmacist')
@login_required
def pharmacist_ai():
    return render_template('pharmacist/ai_assistant.html')

@bp.route("/analyze/patient", methods=["POST"])
@login_required
def analyze_patient():
    """Main endpoint for patient symptom analysis"""
    data = request.get_json(force=True)
    symptoms = data.get("symptoms", "")
    lat = data.get("lat")
    lng = data.get("lng")

    if not symptoms or len(symptoms) < 5:
        return jsonify({"error": "Please provide detailed symptoms"}), 400

    result = PatientAgent.analyze(symptoms, lat, lng)
    return jsonify(result)

@bp.route("/analyze/doctor", methods=["POST"])
@login_required
@role_required("doctor")
def analyze_doctor():
    """Professional clinical support for doctors"""
    data = request.get_json(force=True)
    case_input = data.get("input", "")

    if not case_input or len(case_input) < 10:
        return jsonify({"error": "Please provide more clinical details"}), 400

    result = DoctorAgent.analyze(case_input)
    return jsonify(result)

@bp.route("/analyze/pharmacist", methods=["POST"])
@login_required
@role_required("pharmacist")
def analyze_pharmacist():
    """Medication analysis for pharmacists - alternatives and dosages"""
    from app.agents.pharmacist_agent import PharmacistAgent
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        data = request.get_json(force=True)
        drug_input = data.get("input", "")

        if not drug_input or len(drug_input) < 2:
            return jsonify({"error": "Please provide a medication name"}), 400

        logger.info(f"Pharmacist AI analyzing: {drug_input}")
        result = PharmacistAgent.analyze(drug_input)
        
        # Ensure result is a dictionary
        if not isinstance(result, dict):
            logger.error(f"Agent returned non-dict type: {type(result)}")
            return jsonify({"error": "Internal error: invalid response format"}), 500
            
        # Check if error was returned
        if "error" in result:
            logger.warning(f"Agent returned error: {result['error']}")
            return jsonify(result), 500
            
        return jsonify(result)
    except Exception as e:
        logger.exception(f"Error in pharmacist AI analysis: {str(e)}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

