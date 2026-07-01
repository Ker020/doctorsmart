"""
Permission decorators for role-based access control and resource access validation.
"""
from functools import wraps
from flask import redirect, url_for, flash, session, abort
from flask_login import current_user

def role_required(*roles):
    """
    Decorator to restrict route access to specific user roles.
    
    Usage:
        @bp.route('/admin/dashboard')
        @login_required
        @role_required('admin')
        def admin_dashboard():
            ...
            
        @bp.route('/medical/records')
        @login_required
        @role_required('doctor', 'pharmacist')
        def medical_records():
            ...
    
    Args:
        *roles: Variable number of role strings ('admin', 'doctor', 'pharmacist', 'patient')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify
            if not current_user.is_authenticated:
                if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error': 'Please log in to access this feature'}), 401
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error': 'You do not have permission to access this feature'}), 403
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('auth.login'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def qr_access_required(patient_id_param='patient_id'):
    """
    Decorator to ensure QR-based access was granted for viewing patient data.
    Checks session for QR access token.
    
    Usage:
        @bp.route('/doctor/patient/<int:patient_id>')
        @login_required
        @role_required('doctor')
        @qr_access_required('patient_id')
        def view_patient(patient_id):
            ...
    
    Args:
        patient_id_param: Name of the route parameter containing patient_id
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            patient_id = kwargs.get(patient_id_param)
            
            # Check if QR access was granted for this patient
            qr_accessed_patients = session.get('qr_accessed_patients', [])
            
            # Admin and the patient themselves always have access
            if current_user.role == 'admin':
                return f(*args, **kwargs)
            
            if hasattr(current_user, 'patient_profile') and current_user.patient_profile:
                if current_user.patient_profile.id == patient_id:
                    return f(*args, **kwargs)
            
            # For doctors and pharmacists, check QR access
            if patient_id not in qr_accessed_patients:
                flash('QR code access required to view this patient.', 'error')
                return redirect(url_for(f'{current_user.role}.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def prescription_access_required(prescription_id_param='prescription_id'):
    """
    Decorator to ensure user has access to a specific prescription.
    
    Access rules:
    - Doctor who created the prescription
    - Patient who owns the prescription
    - Pharmacist (can view all prescriptions)
    - Admin (can view all)
    
    Usage:
        @bp.route('/prescription/<int:prescription_id>')
        @login_required
        @prescription_access_required('prescription_id')
        def view_prescription(prescription_id):
            ...
    
    Args:
        prescription_id_param: Name of the route parameter containing prescription_id
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.models.medical_records import Prescription
            
            prescription_id = kwargs.get(prescription_id_param)
            prescription = Prescription.query.get_or_404(prescription_id)
            
            # Admin has access to everything
            if current_user.role == 'admin':
                return f(*args, **kwargs)
            
            # Pharmacists can view all prescriptions
            if current_user.role == 'pharmacist':
                return f(*args, **kwargs)
            
            # Doctor who created the prescription
            if current_user.role == 'doctor' and hasattr(current_user, 'doctor_profile'):
                if prescription.doctor_id == current_user.doctor_profile.id:
                    return f(*args, **kwargs)
            
            # Patient who owns the prescription
            if current_user.role == 'patient' and hasattr(current_user, 'patient_profile'):
                if prescription.patient_id == current_user.patient_profile.id:
                    return f(*args, **kwargs)
            
            # No access
            flash('You do not have permission to access this prescription.', 'error')
            abort(403)
        
        return decorated_function
    return decorator


def grant_qr_access(patient_id):
    """
    Grant QR-based access to a patient's records.
    Stores patient_id in session.
    
    Usage:
        # In QR scan route
        if token_valid:
            grant_qr_access(patient.id)
            return redirect(url_for('doctor.view_patient', patient_id=patient.id))
    """
    if 'qr_accessed_patients' not in session:
        session['qr_accessed_patients'] = []
    
    if patient_id not in session['qr_accessed_patients']:
        session['qr_accessed_patients'].append(patient_id)
        session.modified = True


def revoke_qr_access(patient_id=None):
    """
    Revoke QR-based access.
    If patient_id is None, revokes all QR access.
    
    Usage:
        # On logout or session timeout
        revoke_qr_access()
    """
    if patient_id is None:
        session['qr_accessed_patients'] = []
    else:
        if 'qr_accessed_patients' in session:
            if patient_id in session['qr_accessed_patients']:
                session['qr_accessed_patients'].remove(patient_id)
    
    session.modified = True
