from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.pharmacy import Pharmacist  
from app.models.lab import Lab
from app.models.appointment import Appointment
from app.models.payment import Payment
from datetime import datetime, timedelta
from collections import Counter
import json

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('auth.login'))
    
    # Gather statistics
    stats = {
        'total_users': User.query.count(),
        'total_doctors': Doctor.query.count(),
        'total_appointments': Appointment.query.count(),
        'total_revenue': db.session.query(db.func.sum(Payment.amount)).filter(
            Payment.status == 'completed'
        ).scalar() or 0
    }
    
    # Get all users, doctors, labs, pharmacists
    users = User.query.order_by(User.created_at.desc()).all()
    doctors = Doctor.query.all()
    labs = Lab.query.all()
    pharmacists = Pharmacist.query.all()
    
    # Prepare chart data
    # Appointments over last 7 days
    today = datetime.now().date()
    appointment_labels = []
    appointment_counts = []
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = Appointment.query.filter(
            db.func.date(Appointment.appointment_date) == date
        ).count()
        appointment_labels.append(date.strftime('%b %d'))
        appointment_counts.append(count)
    
    # Specialty distribution
    specialties = [doc.specialty for doc in doctors]
    specialty_counter = Counter(specialties)
    specialty_labels = list(specialty_counter.keys())
    specialty_counts = list(specialty_counter.values())
    
    chart_data = {
        'appointment_labels': appointment_labels,
        'appointment_counts': appointment_counts,
        'specialty_labels': specialty_labels,
        'specialty_counts': specialty_counts
    }
    
    # Fetch pending deletion requests
    from app.models.medical_records import MedicalReport
    deletion_requests = MedicalReport.query.filter_by(deletion_requested=True).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         users=users, 
                         doctors=doctors,
                         labs=labs,
                         pharmacists=pharmacists,
                         chart_data=chart_data,
                         deletion_requests=deletion_requests,
                         user=current_user)

@bp.route('/add_doctor', methods=['POST'])
@login_required
def add_doctor():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    specialty = request.form.get('specialty')
    price = request.form.get('price')
    bio = request.form.get('bio')
    
    # Check existing user
    if User.query.filter_by(email=email).first():
        flash('Email already exists', 'error')
        return redirect(url_for('admin.dashboard'))

    # Create User
    user = User(name=name, email=email, role='doctor')
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    # Create Profile
    default_slots = [
        {"day": "Sunday", "times": ["10:00", "11:00", "14:00", "15:00"]},
        {"day": "Monday", "times": ["10:00", "11:00", "14:00", "15:00"]},
        {"day": "Tuesday", "times": ["10:00", "11:00", "14:00", "15:00"]},
        {"day": "Wednesday", "times": ["10:00", "11:00", "14:00", "15:00"]},
        {"day": "Thursday", "times": ["10:00", "11:00", "14:00", "15:00"]}
    ]
    locations = [{"name": "Main Clinic", "address": "Downtown Medical Center"}]
    
    doctor = Doctor(
        user_id=user.id,
        specialty=specialty,
        license_number=f"LIC-{user.id}",
        price=float(price) if price else 100.0,
        bio=bio,
        locations=locations,
        available_slots=default_slots,
        rating=4.5,
        total_patients=0,
        is_featured=False
    )
    db.session.add(doctor)
    db.session.commit()
    
    flash('Doctor added successfully', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if user_id:
            # Edit existing user
            user = User.query.get(user_id)
            if not user:
                flash('User not found', 'error')
                return redirect(url_for('admin.dashboard'))
            
            if name: user.name = name
            if email:
                if email != user.email:
                    existing = User.query.filter_by(email=email).first()
                    if existing:
                        flash("Email already exists", "error")
                        return redirect(url_for("admin.dashboard"))
                user.email = email
            # We don't usually change role on edit to avoid breaking profile links, but MVP allows basic
            if role: user.role = role
            if password: user.set_password(password)
            
            # Update Profile Data if applicable
            if role == 'doctor':
                if not user.doctor_profile:
                    # Upgrade to doctor if no profile
                     user.doctor_profile = Doctor(user_id=user.id, specialty='General', license_number=f"LIC-{user.id}", price=200.0)
                
                doc = user.doctor_profile
                spec = request.form.get('specialty')
                price = request.form.get('price')
                bio = request.form.get('bio')
                locs = request.form.get('locations')
                if spec: doc.specialty = spec
                if price: doc.price = float(price)
                if bio: doc.bio = bio
                if locs: doc.locations = [{"name": "Main Clinic", "address": loc.strip()} for loc in locs.split(',')]
            
            elif role == 'pharmacist':
                # Similar logic for pharmacist
                # Check import locally to avoid circular dependency if any
                from app.models.pharmacy import Pharmacist
                if not user.pharmacist_profile:
                     user.pharmacist_profile = Pharmacist(user_id=user.id, pharmacy_name="New Pharmacy", license_number=f"PH-{user.id}")
                
                pharma = user.pharmacist_profile
                p_name = request.form.get('pharmacy_name')
                p_addr = request.form.get('pharmacy_address')
                if p_name: pharma.pharmacy_name = p_name
                # Address handling if model supports it (Pharmacist model in current view only has name/license, assuming ext)
                # If model doesn't have address, we skip or add it. Based on previous view, it has pharmacy_name and license.
                # Adding address to model might be needed, for now we stick to pharmacy_name.
                
        else:
            # Create new user
            if User.query.filter_by(email=email).first():
                flash('Email already exists', 'error')
                return redirect(url_for('admin.dashboard'))
            
            user = User(name=name, email=email, role=role)
            user.set_password(password if password else '123456') # Default per user request
            db.session.add(user)
            db.session.flush()
            
            # Create profile based on role
            if role == 'patient':
                import uuid
                patient = Patient(
                    user_id=user.id,
                    medical_id=str(uuid.uuid4()),
                    dob=datetime(2000, 1, 1).date(),
                    blood_type='O+'
                )
                db.session.add(patient)
            
            elif role == 'doctor':
                # Create detailed doctor profile
                from app.models.doctor import Doctor
                spec = request.form.get('specialty') or 'General Practitioner'
                price = request.form.get('price') or 200.0
                bio = request.form.get('bio') or 'New doctor profile'
                locs_raw = request.form.get('locations')
                locations = [{"name": "Main Clinic", "address": loc.strip()} for loc in locs_raw.split(',')] if locs_raw else [{"name": "Main Clinic", "address": "General Hospital"}]

                doctor = Doctor(
                    user_id=user.id,
                    specialty=spec,
                    license_number=f'LIC-{user.id}-{datetime.now().strftime("%Y%m")}',
                    price=float(price),
                    bio=bio,
                    rating=5.0,
                    total_patients=0,
                    locations=locations,
                    available_slots=[]
                )
                db.session.add(doctor)

            elif role == 'pharmacist':
                from app.models.pharmacy import Pharmacist
                p_name = request.form.get('pharmacy_name') or 'Main Pharmacy'
                # p_address not in model yet, ignoring
                
                pharmacist = Pharmacist(
                    user_id=user.id,
                    pharmacy_name=p_name,
                    license_number=f'PH-{user.id}-{datetime.now().strftime("%Y%m")}'
                    # address field is missing in model, skipping
                )
                db.session.add(pharmacist)

            elif role == 'lab':
                from app.models.lab import Lab
                l_name = request.form.get('lab_name') or 'Main Lab'
                lab = Lab(
                    user_id=user.id,
                    name=l_name,
                    address="Lab Address TBD",
                    license_number=f"LAB-{user.id}"
                )
                db.session.add(lab)
        
        db.session.commit()
        flash('User saved successfully', 'success')
        return redirect(url_for('admin.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))

@bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        if user.role == 'admin':
            return jsonify({'success': False, 'error': 'Cannot delete admin users'}), 403
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/toggle_featured/<int:doctor_id>', methods=['POST'])
@login_required
def toggle_featured(doctor_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'success': False, 'error': 'Doctor not found'}), 404
        
        data = request.get_json(silent=True) or {}
        doctor.is_featured = data.get('is_featured', False)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/toggle_user_status/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    """Toggle user active/blocked status"""
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        if user.role == 'admin':
            return jsonify({'success': False, 'error': 'Cannot block admin users'}), 403
        
        data = request.get_json()
        user.is_active = data.get('is_active', True)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# -- Medical Record Deletion Requests --
@bp.route('/authorize_deletion')
@login_required
def authorize_deletion():
    # Helper to check requests (called via ajax or included in dashboard)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'success': True})

@bp.route('/approve_delete_request/<int:report_id>', methods=['POST'])
@login_required
def approve_delete_request(report_id):
    if current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('admin.dashboard'))
    
    from app.models.medical_records import MedicalReport
    report = MedicalReport.query.get_or_404(report_id)
    
    try:
        db.session.delete(report)
        db.session.commit()
        flash('Medical record deleted permanently.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting record: {str(e)}', 'error')
        
    return redirect(url_for('admin.dashboard'))

@bp.route('/reject_delete_request/<int:report_id>', methods=['POST'])
@login_required
def reject_delete_request(report_id):
    if current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('admin.dashboard'))
    
    from app.models.medical_records import MedicalReport
    report = MedicalReport.query.get_or_404(report_id)
    
    try:
        report.deletion_requested = False
        report.deletion_reason = None
        db.session.commit()
        flash('Deletion request rejected.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error rejecting request: {str(e)}', 'error')
        
    return redirect(url_for('admin.dashboard'))

@bp.route('/complaints')
@login_required
def complaints():
    """View all complaints"""
    if current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('admin.dashboard'))
        
    from app.models.complaint import Complaint
    complaints_list = Complaint.query.order_by(Complaint.created_at.desc()).all()
    
    return render_template('admin/complaints.html', complaints=complaints_list, filter_role='all')

@bp.route('/complaints/doctors')
@login_required
def complaints_doctors():
    """View doctor complaints"""
    if current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('admin.dashboard'))
        
    from app.models.complaint import Complaint
    complaints_list = Complaint.query.filter_by(target_role='doctor')\
                                     .order_by(Complaint.created_at.desc()).all()
    
    return render_template('admin/complaints.html', complaints=complaints_list, filter_role='doctor')

@bp.route('/complaints/labs')
@login_required
def complaints_labs():
    """View lab complaints"""
    if current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('admin.dashboard'))
        
    from app.models.complaint import Complaint
    complaints_list = Complaint.query.filter_by(target_role='lab')\
                                     .order_by(Complaint.created_at.desc()).all()
    
    return render_template('admin/complaints.html', complaints=complaints_list, filter_role='lab')

@bp.route('/complaints/pharmacists')
@login_required
def complaints_pharmacists():
    """View pharmacist complaints"""
    if current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('admin.dashboard'))
        
    from app.models.complaint import Complaint
    complaints_list = Complaint.query.filter_by(target_role='pharmacist')\
                                     .order_by(Complaint.created_at.desc()).all()
    
    return render_template('admin/complaints.html', complaints=complaints_list, filter_role='pharmacist')

@bp.route('/complaint/<int:complaint_id>')
@login_required
def view_complaint(complaint_id):
    """View and respond to a specific complaint"""
    if current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('admin.dashboard'))
        
    from app.models.complaint import Complaint
    complaint = Complaint.query.get_or_404(complaint_id)
    
    return render_template('admin/complaint_detail.html', complaint=complaint)

@bp.route('/complaint/<int:complaint_id>/respond', methods=['POST'])
@login_required
def respond_complaint(complaint_id):
    """Submit response to a complaint"""
    if current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('admin.dashboard'))
        
    from app.models.complaint import Complaint
    complaint = Complaint.query.get_or_404(complaint_id)
    
    response_text = request.form.get('response')
    if not response_text:
        flash('Please enter a response', 'error')
        return redirect(url_for('admin.view_complaint', complaint_id=complaint_id))
    
    complaint.admin_response = response_text
    complaint.status = 'Responded'
    complaint.responded_at = datetime.utcnow()
    db.session.commit()
    
    flash('Response submitted successfully', 'success')
    return redirect(url_for('admin.view_complaint', complaint_id=complaint_id))

@bp.route('/promote_user', methods=['POST'])
@login_required
def promote_user():
    """Promote a patient user to a professional role (doctor, pharmacist, lab)"""
    if current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('admin.dashboard'))
    
    try:
        user_id = request.form.get('user_id')
        new_role = request.form.get('role')
        
        user = User.query.get(user_id)
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('admin.dashboard'))
        
        # Update user role
        user.role = new_role
        
        # Create appropriate profile based on new role
        if new_role == 'doctor':
            specialty = request.form.get('specialty') or 'General Practitioner'
            price = request.form.get('price') or 200.0
            
            doctor = Doctor(
                user_id=user.id,
                specialty=specialty,
                license_number=f'LIC-{user.id}-{datetime.now().strftime("%Y%m")}',
                price=float(price),
               bio='New doctor profile',
                rating=5.0,
                total_patients=0,
                locations=[{"name": "Main Clinic", "address": "General Hospital"}],
                available_slots=[]
            )
            db.session.add(doctor)
            
        elif new_role == 'pharmacist':
            pharmacy_name = request.form.get('pharmacy_name') or 'Main Pharmacy'
            pharmacist = Pharmacist(
                user_id=user.id,
                pharmacy_name=pharmacy_name,
                license_number=f'PH-{user.id}-{datetime.now().strftime("%Y%m")}'
            )
            db.session.add(pharmacist)
            
        elif new_role == 'lab':
            lab_name = request.form.get('lab_name') or 'Main Lab'
            lab = Lab(
                user_id=user.id,
                name=lab_name,
                address="Lab Address TBD",
                license_number=f"LAB-{user.id}"
            )
            db.session.add(lab)
        
        db.session.commit()
        flash(f'User promoted to {new_role} successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error promoting user: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))
