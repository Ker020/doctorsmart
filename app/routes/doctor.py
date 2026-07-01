from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app, session
from flask_login import login_required, current_user
from app.models.chat import QRToken
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.medical_records import MedicalReport, Prescription, LabTest
from app.models.prescription_modification import PrescriptionModification
from app.models.audit import AuditLog
from app.utils.qr import generate_qr_token, create_qr_image
from app.utils.decorators import role_required, grant_qr_access, prescription_access_required
from app.agents.doctor_agent import DoctorAgent
from app.extensions import db
from datetime import datetime, timedelta

bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@bp.route('/dashboard')
@login_required
@role_required('doctor')
def dashboard():
    # Get confirmed appointments for today and onwards
    appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.doctor_profile.id,
        Appointment.status == 'confirmed',
        Appointment.appointment_date >= datetime.now().replace(hour=0, minute=0, second=0)
    ).order_by(Appointment.appointment_date.asc()).all()

    # Get pending modification requests for this doctor
    pending_modifications = PrescriptionModification.query.join(
        Prescription
    ).filter(
        Prescription.doctor_id == current_user.doctor_profile.id,
        PrescriptionModification.status == 'pending'
    ).order_by(PrescriptionModification.created_at.desc()).all()
    
    return render_template('doctor/dashboard.html', 
                         user=current_user,
                         appointments=appointments,
                         pending_modifications=pending_modifications)

@bp.route('/scan_qr_page')
@login_required
@role_required('doctor')
def scan_qr_page():
    return render_template('shared/scan_qr.html', post_url=url_for('doctor.scan_qr'))

@bp.route('/scan_qr', methods=['POST'])
@login_required
@role_required('doctor')
def scan_qr():
    # In production this comes from a camera/scanner
    token_str = request.form.get('token')
    
    token_entry = QRToken.query.filter_by(token_hash=token_str).first()
    if not token_entry:
        current_app.logger.warning(f"QR Scan: Token {token_str[:10]}... not found.")
        flash('Invalid QR code', 'error')
        return redirect(url_for('doctor.dashboard'))
        
    if not token_entry.is_valid():
        current_app.logger.warning(f"QR Scan: Token {token_str[:10]}... expired at {token_entry.expires_at}.")
        flash('Expired QR code', 'error')
        return redirect(url_for('doctor.dashboard'))
        
    if token_entry.allowed_role not in ['doctor', 'all']:
        flash('Unauthorized QR token', 'error')
        return redirect(url_for('doctor.dashboard'))
    
    # Grant QR access
    grant_qr_access(token_entry.patient_id)
    
    # Log access
    AuditLog.log(
        user_id=current_user.id,
        action='qr_access_granted',
        resource_type='patient',
        resource_id=token_entry.patient_id
    )
    db.session.commit()
        
    # Valid - Redirect to view patient
    patient = Patient.query.get(token_entry.patient_id)
    return redirect(url_for('doctor.view_patient', patient_id=patient.id))

@bp.route('/patient/<int:patient_id>')
@login_required
@role_required('doctor')
def view_patient(patient_id):
    # Check QR access
    qr_accessed_patients = session.get('qr_accessed_patients', [])
    if patient_id not in qr_accessed_patients:
        flash('QR code access required to view this patient.', 'error')
        return redirect(url_for('doctor.dashboard'))
        
    patient = Patient.query.get_or_404(patient_id)
    history = MedicalReport.query.filter_by(patient_id=patient_id).order_by(MedicalReport.created_at.desc()).all()
    lab_tests = LabTest.query.filter_by(patient_id=patient_id).order_by(LabTest.ordered_date.desc()).all()
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).order_by(Prescription.created_at.desc()).all()
    
    # Generate AI insights from history
    ai_insights = None
    if history:
        history_summary = "; ".join([f"{r.diagnosis}: {(r.description or '')[:100]}" for r in history[:3]])
        ai_insights = DoctorAgent.assist_diagnosis("Analyze history for clinical insights.", history_summary)
    
    # Pre-serialize lab tests for JS
    lab_tests_json = []
    for test in lab_tests:
        lab_tests_json.append({
            'id': test.id,
            'test_name': test.test_name,
            'test_type': test.test_type,
            'results': test.results,
            'completed_date': test.completed_date.strftime('%d %b %Y %H:%M') if test.completed_date else None
        })

    return render_template('doctor/view_patient.html', 
                          patient=patient, 
                          history=history,
                          lab_tests=lab_tests,
                          lab_tests_json=lab_tests_json,
                          prescriptions=prescriptions,
                          ai_insights=ai_insights)

@bp.route('/add_diagnosis', methods=['POST'])
@login_required
def add_diagnosis():
    patient_id = request.form.get('patient_id')
    diagnosis = request.form.get('diagnosis')
    notes = request.form.get('notes')
    

    if not current_user.doctor_profile:
        # Fallback: Create profile if missing (Lazy Creation)
        from app.models.doctor import Doctor
        new_profile = Doctor(
            user_id=current_user.id,
            specialty='General',
            license_number=f'AUTO-{current_user.id}',
            price=0.0
        )
        db.session.add(new_profile)
        db.session.commit()
        # Refresh user to get the relationship
        db.session.refresh(current_user)

    new_entry = MedicalReport(
        patient_id=patient_id,
        doctor_id=current_user.doctor_profile.id,
        title=f"Diagnosis: {diagnosis[:30] if diagnosis else 'General Checkup'}",
        report_type='diagnosis',
        diagnosis=diagnosis,
        description=notes,
        created_at=datetime.utcnow()
    )
    db.session.add(new_entry)
    db.session.commit()
    
    return redirect(url_for('doctor.view_patient', patient_id=patient_id))

@bp.route('/ai_assist', methods=['POST'])
@login_required
def ai_assist():
    data = request.get_json()
    symptoms = data.get('symptoms')
    history = data.get('history')
    response = DoctorAgent.assist_diagnosis(symptoms, history)
    return jsonify({'advice': response})

@bp.route('/request_delete_report/<int:report_id>', methods=['POST'])
@login_required
def request_delete_report(report_id):
    if current_user.role != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
        
    report = MedicalReport.query.get_or_404(report_id)
    
    report.deletion_requested = True
    report.deletion_reason = 'Doctor requested deletion'
    db.session.commit()
    
    flash('Deletion request submitted to Admin.', 'info')
    return redirect(request.referrer)

@bp.route('/add_prescription', methods=['POST'])
@login_required
def add_prescription():
    if current_user.role != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
        
    patient_id = request.form.get('patient_id')
    diagnosis = request.form.get('diagnosis')
    meds_str = request.form.get('medications')
    instructions = request.form.get('instructions')
    
    # Simple medications parsing (med name - dose - freq)
    meds_list = []
    if meds_str:
        for line in meds_str.split('\n'):
            if '-' in line:
                parts = line.split('-')
                meds_list.append({
                    'name': parts[0].strip(),
                    'dosage': parts[1].strip() if len(parts) > 1 else '',
                    'frequency': parts[2].strip() if len(parts) > 2 else ''
                })
    
    new_prescription = Prescription(
        patient_id=patient_id,
        doctor_id=current_user.doctor_profile.id,
        diagnosis=diagnosis,
        medications=meds_list,
        instructions=instructions,
        created_at=datetime.utcnow(),
        status='active'
    )
    db.session.add(new_prescription)
    db.session.commit()
    
    # Log the action
    AuditLog.log(
        user_id=current_user.id,
        action='prescription_created',
        resource_type='prescription',
        resource_id=new_prescription.id,
        details={'patient_id': patient_id, 'diagnosis': diagnosis}
    )
    db.session.commit()
    
    flash('Prescription added successfully!', 'success')
    return redirect(url_for('doctor.view_patient', patient_id=patient_id))

# ===== Prescription Modification Management =====

@bp.route('/modifications/pending')
@login_required
@role_required('doctor')
def pending_modifications():
    """View all pending modification requests for this doctor's prescriptions"""
    modifications = PrescriptionModification.query.join(
        Prescription
    ).filter(
        Prescription.doctor_id == current_user.doctor_profile.id,
        PrescriptionModification.status == 'pending'
    ).order_by(PrescriptionModification.created_at.desc()).all()
    
    return render_template('doctor/modifications.html', modifications=modifications)

@bp.route('/modification/<int:modification_id>/approve', methods=['POST'])
@login_required
@role_required('doctor')
def approve_modification(modification_id):
    """Approve a pharmacist's modification request"""
    modification = PrescriptionModification.query.get_or_404(modification_id)
    
    # Verify this doctor owns the prescription
    if modification.prescription.doctor_id != current_user.doctor_profile.id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('doctor.dashboard'))
    
    doctor_notes = request.form.get('doctor_response', '')
    
    # Approve the modification (updates prescription automatically)
    modification.approve(doctor_notes)
    
    # Log the action
    AuditLog.log(
        user_id=current_user.id,
        action='prescription_modification_approved',
        resource_type='prescription_modification',
        resource_id=modification_id,
        details={
            'prescription_id': modification.prescription_id,
            'pharmacist_id': modification.pharmacist_id,
            'response': doctor_notes
        }
    )
    
    db.session.commit()
    
    flash('Modification approved successfully!', 'success')
    return redirect(url_for('doctor.pending_modifications'))

@bp.route('/modification/<int:modification_id>/reject', methods=['POST'])
@login_required
@role_required('doctor')
def reject_modification(modification_id):
    """Reject a pharmacist's modification request"""
    modification = PrescriptionModification.query.get_or_404(modification_id)
    
    # Verify this doctor owns the prescription
    if modification.prescription.doctor_id != current_user.doctor_profile.id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('doctor.dashboard'))
    
    doctor_notes = request.form.get('doctor_response', '')
    
    # Reject the modification
    modification.reject(doctor_notes)
    
    # Log the action
    AuditLog.log(
        user_id=current_user.id,
        action='prescription_modification_rejected',
        resource_type='prescription_modification',
        resource_id=modification_id,
        details={
            'prescription_id': modification.prescription_id,
            'pharmacist_id': modification.pharmacist_id,
            'response': doctor_notes
        }
    )
    
    db.session.commit()
    
    flash('Modification rejected.', 'info')
    return redirect(url_for('doctor.pending_modifications'))

@bp.route('/prescription/<int:prescription_id>')
@login_required
@role_required('doctor')
@prescription_access_required('prescription_id')
def view_prescription(prescription_id):
    """View prescription details with modification history"""
    prescription = Prescription.query.get_or_404(prescription_id)
    
    # Get modification history
    modifications = PrescriptionModification.query.filter_by(
        prescription_id=prescription_id
    ).order_by(PrescriptionModification.created_at.desc()).all()
    
    return render_template('doctor/view_prescription.html',
                         prescription=prescription,
                         modifications=modifications)
@bp.route('/appointment/<int:appointment_id>/complete', methods=['POST'])
@login_required
@role_required('doctor')
def complete_appointment(appointment_id):
    """Mark an appointment as completed"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.doctor_id != current_user.doctor_profile.id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('doctor.dashboard'))
        
    appointment.status = 'completed'
    db.session.commit()
    
    flash('Appointment marked as completed.', 'success')
    return redirect(url_for('doctor.dashboard'))

@bp.route('/update_availability', methods=['POST'])
@login_required
@role_required('doctor')
def update_availability():
    """Update doctor's working hours"""
    try:
        data = request.get_json()
        slots = data.get('slots')
        
        doctor = current_user.doctor_profile
        doctor.available_slots = slots
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Availability updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
