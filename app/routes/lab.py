from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session
from flask_login import login_required, current_user
from app.extensions import db
from app.models.lab import Lab, LabService, LabTestType, LabAppointment
from app.models.patient import Patient
from app.models.medical_records import LabTest
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.models.chat import QRToken
from app.utils.decorators import grant_qr_access
from app.models.audit import AuditLog

bp = Blueprint('lab', __name__, url_prefix='/lab')

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role != 'lab':
        flash('Unauthorized', 'error')
        return redirect(url_for('auth.login'))
    
    lab = current_user.lab_profile
    if not lab:
        flash('Lab profile not found', 'error')
        return redirect(url_for('auth.logout'))
        
    # Handle Hours Update
    if request.method == 'POST' and 'update_hours' in request.form:
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        days = request.form.getlist('days')
        
        lab.available_slots = {
            "start": start_time,
            "end": end_time,
            "days": days
        }
        db.session.commit()
        flash('Working hours updated successfully', 'success')
        return redirect(url_for('lab.dashboard'))

    appointments = LabAppointment.query.filter_by(lab_id=lab.id).order_by(LabAppointment.appointment_date).all()
    today_count = LabAppointment.query.filter(
        LabAppointment.lab_id == lab.id,
        db.func.date(LabAppointment.appointment_date) == datetime.utcnow().date()
    ).count()
    
    return render_template('lab/dashboard.html', 
                         lab=lab, 
                         appointments=appointments,
                         today_count=today_count)

@bp.route('/services')
@login_required
def services():
    if current_user.role != 'lab':
        return redirect(url_for('auth.login'))
        
    lab = current_user.lab_profile
    my_services = LabService.query.filter_by(lab_id=lab.id).all()
    all_test_types = LabTestType.query.order_by(LabTestType.name).all()
    
    return render_template('lab/services.html', services=my_services, test_types=all_test_types)

@bp.route('/add_service', methods=['POST'])
@login_required
def add_service():
    if current_user.role != 'lab':
        return redirect(url_for('auth.login'))
        
    lab = current_user.lab_profile
    test_type_id = request.form.get('test_type_id')
    price = request.form.get('price')
    instructions = request.form.get('instructions')
    turnaround = request.form.get('turnaround')
    
    # Check if already exists
    existing = LabService.query.filter_by(lab_id=lab.id, test_type_id=test_type_id).first()
    if existing:
        flash('Service already offered, please edit instead.', 'warning')
        return redirect(url_for('lab.services'))
        
    new_service = LabService(
        lab_id=lab.id,
        test_type_id=test_type_id,
        price=float(price),
        preparation_instructions=instructions,
        turnaround_time=turnaround
    )
    db.session.add(new_service)
    db.session.commit()
    
    flash('Service added successfully', 'success')
    return redirect(url_for('lab.services'))

@bp.route('/delete_service/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    service = LabService.query.get_or_404(service_id)
    if service.lab_id != current_user.lab_profile.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('lab.services'))

@bp.route('/upload_result/<int:appointment_id>', methods=['POST'])
@login_required
def upload_result(appointment_id):
    if current_user.role != 'lab':
        return jsonify({'error': 'Unauthorized'}), 403
        
    appointment = LabAppointment.query.get_or_404(appointment_id)
    if appointment.lab_id != current_user.lab_profile.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('lab.dashboard'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('lab.dashboard'))
        
    if file:
        filename = secure_filename(file.filename)
        unique_name = f"lab_{appointment.id}_{datetime.utcnow().timestamp()}_{filename}"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        path = os.path.join(upload_folder, unique_name)
        file.save(path)
        
        # Update Appointment
        appointment.result_file = unique_name
        appointment.status = 'Completed'
        appointment.result_notes = request.form.get('notes', '')
        
        # Create a Medical Record (LabTest) for the patient so it appears in their history
        lab_test = LabTest(
            patient_id=appointment.patient_id,
            test_name=appointment.service.test_type.name,
            test_type='Lab Result',
            status='completed',
            results=f"Completed by {current_user.lab_profile.name}. {appointment.result_notes}",
            file_path=unique_name,
            ordered_date=appointment.appointment_date,
            completed_date=datetime.utcnow()
        )
        db.session.add(lab_test)
        db.session.commit()
        
        flash('Result uploaded and sent to patient.', 'success')
        
    return redirect(url_for('lab.dashboard'))

@bp.route('/scan_qr_page')
@login_required
def scan_qr_page():
    if current_user.role != 'lab':
        return redirect(url_for('auth.login'))
    return render_template('shared/scan_qr.html', post_url=url_for('lab.scan_qr'))

@bp.route('/scan_qr', methods=['POST'])
@login_required
def scan_qr():
    if current_user.role != 'lab':
        flash('Unauthorized', 'error')
        return redirect(url_for('lab.dashboard'))
        
    token_str = request.form.get('token')
    
    token_entry = QRToken.query.filter_by(token_hash=token_str).first()
    if not token_entry or not token_entry.is_valid():
        flash('Invalid or expired QR code', 'error')
        return redirect(url_for('lab.scan_qr_page'))
    
    # Grant access
    grant_qr_access(token_entry.patient_id)
    
    AuditLog.log(
        user_id=current_user.id,
        action='qr_access_granted',
        resource_type='patient',
        resource_id=token_entry.patient_id
    )
    db.session.commit()
    
    return redirect(url_for('lab.view_patient', patient_id=token_entry.patient_id))

@bp.route('/patient/<int:patient_id>')
@login_required
def view_patient(patient_id):
    if current_user.role != 'lab':
        return redirect(url_for('auth.login'))
        
    # Check access
    if patient_id not in session.get('qr_accessed_patients', []):
        flash('QR Access Required. Please scan patient QR code.', 'warning')
        return redirect(url_for('lab.scan_qr_page'))
        
    patient = Patient.query.get_or_404(patient_id)
    history = LabTest.query.filter_by(patient_id=patient_id).order_by(LabTest.ordered_date.desc()).all()
    upcoming_appointments = LabAppointment.query.filter_by(patient_id=patient_id, status='Confirmed').all()
    
    return render_template('lab/view_patient.html', 
                         patient=patient, 
                         history=history,
                         appointments=upcoming_appointments,
                         now=lambda: datetime.utcnow().date())
