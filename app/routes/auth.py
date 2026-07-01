from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, login_manager
from app.models.user import User
from app.models.patient import Patient
import uuid
from datetime import datetime

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_based_on_role(current_user)
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect_based_on_role(user)
        else:
            flash('Invalid email or password', 'error')
            
    return render_template('auth.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect_based_on_role(current_user)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role') # patient, doctor, pharmacist
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
            
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # If Patient, create profile automatically
        if role == 'patient':
            # Demo values for MVP + Form Data
            weight = request.form.get('weight')
            height = request.form.get('height')
            chronic = request.form.get('chronic_diseases')
            
            patient_profile = Patient(
                user_id=new_user.id,
                medical_id=str(uuid.uuid4()),
                dob=datetime.utcnow().date(), # Placeholder for sim
                blood_type='O+', # Placeholder
                weight=float(weight) if weight else None,
                height=float(height) if height else None,
                chronic_diseases=chronic
            )
            db.session.add(patient_profile)
            db.session.commit()
        
        elif role == 'lab':
             from app.models.lab import Lab
             lab = Lab(user_id=new_user.id, name=name, address="TBD", license_number=f"LAB-{new_user.id}")
             db.session.add(lab)
             db.session.commit()

        login_user(new_user)
        return redirect_based_on_role(new_user)
        
    return render_template('auth.html', register=True) # Reuse auth.html

@bp.route('/switch_role/<role>')
@login_required
def switch_role(role):
    from flask import session
    
    # Check if user is allowed to switch (not a basic patient)
    if current_user.role == 'patient' and role != 'patient':
        flash('Unauthorized role switch', 'error')
        return redirect(url_for('patient.dashboard'))
    
    # If switching to patient view, set active_role in session
    if role == 'patient':
        session['active_role'] = 'patient'
        # If no profile, we will be redirected by the dashboard route itself 
        # but let's be explicit and check here too if we want a smoother experience
        if not current_user.patient_profile:
             flash('Please complete your patient profile details first.', 'info')
        return redirect(url_for('patient.dashboard'))
    else:
        # Clear the patient view override
        session.pop('active_role', None)
        return redirect_based_on_role(current_user)

@bp.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    if current_user.patient_profile:
        return redirect(url_for('patient.dashboard'))
        
    if request.method == 'POST':
        dob = request.form.get('dob')
        blood_type = request.form.get('blood_type')
        weight = request.form.get('weight')
        height = request.form.get('height')
        chronic = request.form.get('chronic_diseases')
        
        patient_profile = Patient(
            user_id=current_user.id,
            medical_id=str(uuid.uuid4()),
            dob=datetime.strptime(dob, '%Y-%m-%d').date() if dob else datetime.utcnow().date(),
            blood_type=blood_type,
            weight=float(weight) if weight else None,
            height=float(height) if height else None,
            chronic_diseases=chronic
        )
        db.session.add(patient_profile)
        db.session.commit()
        flash('Patient profile completed successfully.', 'success')
        return redirect(url_for('patient.dashboard'))
        
    return render_template('patient/complete_profile.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def redirect_based_on_role(user):
    if user.role == 'patient':
        return redirect(url_for('patient.dashboard'))
    elif user.role == 'doctor':
        return redirect(url_for('doctor.dashboard'))
    elif user.role == 'pharmacist':
        return redirect(url_for('pharmacist.dashboard'))
    elif user.role == 'lab':
        return redirect(url_for('lab.dashboard'))
    elif user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))
