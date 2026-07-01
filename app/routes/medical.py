from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.medical_records import MedicalReport, LabTest, Prescription, VitalSigns
from app.models.user import User

bp = Blueprint('medical', __name__, url_prefix='/medical')

@bp.route('/records')
@login_required
def records():
    if current_user.role == 'patient':
        reports = MedicalReport.query.filter_by(patient_id=current_user.patient_profile.id).order_by(MedicalReport.created_at.desc()).all()
        prescriptions = Prescription.query.filter_by(patient_id=current_user.patient_profile.id).order_by(Prescription.created_at.desc()).all()
        lab_tests = LabTest.query.filter_by(patient_id=current_user.patient_profile.id).order_by(LabTest.ordered_date.desc()).all()
        return render_template('patient/medical_records.html', reports=reports, prescriptions=prescriptions, lab_tests=lab_tests)
    else:
        # For doctors/admins to search for a patient
        return render_template('medical/search_patient.html')

@bp.route('/patient/<int:patient_id>')
@login_required
def view_patient_records(patient_id):
    if current_user.role not in ['doctor', 'admin', 'pharmacist']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
        
    patient_user = User.query.get_or_404(patient_id)
    if not patient_user.patient_profile:
         flash('User is not a patient.', 'warning')
         return redirect(url_for('main.index'))
         
    reports = MedicalReport.query.filter_by(patient_id=patient_user.patient_profile.id).order_by(MedicalReport.created_at.desc()).all()
    prescriptions = Prescription.query.filter_by(patient_id=patient_user.patient_profile.id).order_by(Prescription.created_at.desc()).all()
    lab_tests = LabTest.query.filter_by(patient_id=patient_user.patient_profile.id).order_by(LabTest.ordered_date.desc()).all()
    
    return render_template('medical/patient_records.html', patient=patient_user, reports=reports, prescriptions=prescriptions, lab_tests=lab_tests)
