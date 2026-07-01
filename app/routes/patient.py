import json
import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.medical_records import LabTest
from app.models.doctor import Doctor
from app.models.lab import Lab, LabService, LabTestType, LabAppointment
from app.models.chat import QRToken
from app.models.rating import Rating
from app.utils.qr import generate_qr_token, create_qr_image

bp = Blueprint('patient', __name__, url_prefix='/patient')

@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.patient_profile:
        return redirect(url_for('auth.complete_profile'))
    
    patient_id = current_user.patient_profile.id
    
    # Get/Generate QR Token (Valid for both doc/pharmacist)
    active_token = QRToken.query.filter_by(
        patient_id=patient_id,
        allowed_role='all'
    ).order_by(QRToken.created_at.desc()).first()
    
    if not active_token or not active_token.is_valid():
        token_hash = generate_qr_token(patient_id, 'all')
        active_token = QRToken(
            token_hash=token_hash,
            patient_id=patient_id,
            allowed_role='all',
            expires_at=datetime.utcnow() + timedelta(days=36500) # 100 years
        )
        db.session.add(active_token)
        db.session.commit()
    
    qr_filename = f"qr_{current_user.id}.png"
    qr_image = create_qr_image(active_token.token_hash, qr_filename)
    
    # Get recent lab tests for the dashboard
    lab_tests = LabTest.query.filter_by(patient_id=patient_id).order_by(LabTest.completed_date.desc()).limit(5).all()
    
    # Pre-serialize lab tests for JS
    lab_tests_json = []
    for test in lab_tests:
        lab_tests_json.append({
            'id': test.id,
            'test_name': test.test_name,
            'test_type': test.test_type,
            'results': test.results,
            'completed_date': test.completed_date.strftime('%Y-%m-%d %H:%M') if test.completed_date else None
        })
        
    return render_template('patient/dashboard.html', 
                          lab_tests=lab_tests, 
                          lab_tests_json=lab_tests_json,
                          qr_image=qr_image,
                          qr_token=active_token.token_hash)

@bp.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        unique_name = f"{datetime.utcnow().timestamp()}_{filename}"
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        file.save(path)
        
        from app.services.analysis_service import AnalysisService
        service = AnalysisService()
        
        # Prepare patient context for rich analysis
        patient_data = {
            "name": current_user.name,
            "age": (datetime.utcnow().date() - current_user.patient_profile.dob).days // 365 if current_user.patient_profile.dob else 30,
            "gender": 'male', # Defaulting as gender is not in Patient model
            "pregnant": False
        }
        
        analysis_result = service.analyze_lab_report(path, patient_data=patient_data)
        
        # Extract the data part if successful
        final_results = analysis_result.get('data') if analysis_result.get('success') else analysis_result
        
        new_test = LabTest(
            patient_id=current_user.patient_profile.id,
            test_name=f"Uploaded: {filename}",
            test_type='report',
            status='completed',
            results=json.dumps(final_results),
            file_path=unique_name,
            completed_date=datetime.utcnow()
        )
        db.session.add(new_test)
        db.session.commit()
        return jsonify({'success': True, 'filename': unique_name})
    return jsonify({'success': False, 'error': 'Failed to save file'}), 500

@bp.route('/analysis_history')
@login_required
def analysis_history():
    if not current_user.patient_profile:
        flash('Patient profile not found', 'error')
        return redirect(url_for('patient.dashboard'))
        
    lab_tests = LabTest.query.filter_by(patient_id=current_user.patient_profile.id).order_by(LabTest.completed_date.desc()).all()
    
    # Pre-process JSON data for the template
    processed_tests = []
    for test in lab_tests:
        try:
            results_data = json.loads(test.results) if test.results else {}
        except:
            results_data = {}
            
        processed_tests.append({
            'test': test,
            'data': results_data
        })
        
    return render_template('patient/analysis_history.html', tests=processed_tests)

@bp.route('/ratings')
@login_required
def ratings():
    if not current_user.patient_profile:
        flash('Patient profile not found', 'error')
        return redirect(url_for('patient.dashboard'))
    ratings = Rating.query.filter_by(patient_id=current_user.patient_profile.id).all()
    return render_template('patient/ratings.html', ratings=ratings)

@bp.route('/submit_complaint', methods=['GET', 'POST'])
@login_required
def submit_complaint():
    if request.method == 'POST':
        subject = request.form.get('subject')
        description = request.form.get('description')
        target_role = request.form.get('target_role')
        target_id = request.form.get('target_id')
        
        from app.models.complaint import Complaint
        new_complaint = Complaint(
            user_id=current_user.id,
            subject=subject,
            description=description,
            target_role=target_role,
            target_id=int(target_id) if target_id and target_id.isdigit() else None
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash('Complaint submitted successfully.', 'success')
        return redirect(url_for('patient.dashboard'))
        
    from app.models.pharmacy import Pharmacist
    doctors = [{'id': d.id, 'user': {'name': d.user.name}, 'specialty': d.specialty} for d in Doctor.query.all()]
    labs = [{'id': l.id, 'name': l.name} for l in Lab.query.all()]
    pharmacists = [{'id': p.id, 'user': {'name': p.user.name}, 'pharmacy_name': p.pharmacy_name} for p in Pharmacist.query.all()]
    return render_template('patient/submit_complaint.html', doctors=doctors, labs=labs, pharmacists=pharmacists)

@bp.route('/book_lab')
@login_required
def book_lab():
    from app.models.lab import LabService, LabTestType
    services = LabService.query.all()
    test_types = LabTestType.query.all()
    return render_template('patient/book_lab.html', services=services, test_types=test_types)

@bp.route('/confirm_lab_booking/<int:service_id>', methods=['POST'])
@login_required
def confirm_lab_booking(service_id):
    from app.models.lab import LabService, LabAppointment
    service = LabService.query.get_or_404(service_id)
    date_str = request.form.get('appointment_date')
    if not date_str:
        flash('Please select a date', 'error')
        return redirect(url_for('patient.book_lab'))
        
    try:
        appt_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash('Invalid date format', 'error')
        return redirect(url_for('patient.book_lab'))
        
    new_appt = LabAppointment(
        patient_id=current_user.patient_profile.id,
        lab_id=service.lab_id,
        service_id=service_id,
        appointment_date=appt_date,
        status='Confirmed'
    )
    db.session.add(new_appt)
    db.session.commit()
    flash(f'Lab appointment booked for {service.test_type.name}', 'success')
    return redirect(url_for('patient.dashboard'))


@bp.route('/vital_signs')
@login_required
def vital_signs():
    if not current_user.patient_profile:
        return redirect(url_for('patient.dashboard'))
    return render_template('patient/vital_signs.html')