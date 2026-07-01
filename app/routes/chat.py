from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from app.models.chat import ChatMessage
from app.models.medical_records import Prescription
from app.models.appointment import Appointment
from app.models.user import User
from app.extensions import db
from datetime import datetime

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/send', methods=['POST'])
@login_required
def send_message():
    """Send a chat message, optionally linked to a prescription"""
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    content = data.get('message')
    prescription_id = data.get('prescription_id')  # Optional
    
    if not receiver_id or not content:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    msg = ChatMessage(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        message=content,
        prescription_id=prescription_id,
        created_at=datetime.utcnow()
    )
    db.session.add(msg)
    db.session.commit()
    
    return jsonify({'status': 'sent', 'message_id': msg.id})

@bp.route('/get_messages/<int:partner_id>')
@login_required
def get_messages(partner_id):
    """Fetch conversation with a specific user, optionally filtered by prescription"""
    prescription_id = request.args.get('prescription_id', type=int)
    
    # Base query for conversation
    query = ChatMessage.query.filter(
        ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == partner_id)) |
        ((ChatMessage.sender_id == partner_id) & (ChatMessage.receiver_id == current_user.id))
    )
    
    # Filter by prescription if provided
    if prescription_id:
        query = query.filter(ChatMessage.prescription_id == prescription_id)
    
    messages = query.order_by(ChatMessage.created_at.asc()).all()
    
    # Mark messages as read
    for msg in messages:
        if msg.receiver_id == current_user.id and not msg.is_read:
            msg.is_read = True
    db.session.commit()
    
    return jsonify([{
        'id': m.id,
        'sender': m.sender_id,
        'message': m.message,
        'prescription_id': m.prescription_id,
        'timestamp': m.created_at.isoformat(),
        'is_read': m.is_read
    } for m in messages])

@bp.route('/')
@login_required
def index():
    """Main chat interface"""
    # Get prescription context if provided
    prescription_id = request.args.get('prescription_id', type=int)
    partner_id = request.args.get('partner_id', type=int)
    
    prescription = None
    if prescription_id:
        prescription = Prescription.query.get(prescription_id)
    
    partner = None
    if partner_id:
        partner = User.query.get(partner_id)
    
    return render_template('chat/index.html', 
                         prescription=prescription,
                         partner=partner)

@bp.route('/contacts')
@login_required
def get_contacts():
    """Get list of users the current user can chat with"""
    contacts = []
    
    if current_user.role == 'doctor':
        # Doctors can chat with: pharmacists, admins, and their patients
        # Get pharmacists and admins
        contacts = User.query.filter(
            User.id != current_user.id,
            User.role.in_(['pharmacist', 'admin'])
        ).all()
        
        # Get patients from QR-accessed, prescriptions, or confirmed appointments
        patient_ids = []
        
        # QR Accessed
        qr_accessed_patients = session.get('qr_accessed_patients', [])
        patient_ids.extend(qr_accessed_patients)
        
        # Prescription patients
        prescribed_patients = Prescription.query.filter_by(doctor_id=current_user.doctor_profile.id).all()
        patient_ids.extend([p.patient_id for p in prescribed_patients])
        
        # Appointment patients
        appointments = Appointment.query.filter_by(
            doctor_id=current_user.doctor_profile.id,
            status='confirmed'
        ).all()
        patient_ids.extend([a.patient_id for a in appointments])
        
        # Distinct unique patient user objects
        if patient_ids:
            from app.models.patient import Patient
            patients = Patient.query.filter(Patient.id.in_(list(set(patient_ids)))).all()
            contacts.extend([p.user for p in patients])
    
    elif current_user.role == 'pharmacist':
        # Pharmacists can chat with: doctors, admins
        contacts = User.query.filter(
            User.id != current_user.id,
            User.role.in_(['doctor', 'admin'])
        ).all()
    
    elif current_user.role == 'patient':
        # Patients can chat with: their doctors (who prescribed to them or they have appointments with)
        if hasattr(current_user, 'patient_profile') and current_user.patient_profile:
            # Doctors from prescriptions
            prescriptions = Prescription.query.filter_by(
                patient_id=current_user.patient_profile.id
            ).all()
            doctor_user_ids = [p.doctor.user_id for p in prescriptions if p.doctor]
            
            # Doctors from confirmed appointments
            appointments = Appointment.query.filter_by(
                patient_id=current_user.patient_profile.id,
                status='confirmed'
            ).all()
            doctor_user_ids.extend([a.doctor.user_id for a in appointments if a.doctor])
            
            if doctor_user_ids:
                contacts = User.query.filter(User.id.in_(list(set(doctor_user_ids)))).all()
    
    elif current_user.role == 'admin':
        # Admins can chat with everyone
        contacts = User.query.filter(
            User.id != current_user.id,
            User.role.in_(['doctor', 'pharmacist', 'patient'])
        ).all()
    
    # Get unread count for each contact
    contact_list = []
    for c in contacts:
        unread_count = ChatMessage.query.filter_by(
            sender_id=c.id,
            receiver_id=current_user.id,
            is_read=False
        ).count()
        
        contact_list.append({
            'id': c.id,
            'name': c.name,
            'role': c.role,
            'avatar': c.profile_image or 'default_avatar.png',
            'unread_count': unread_count
        })
    
    return jsonify(contact_list)

@bp.route('/prescription/<int:prescription_id>')
@login_required
def prescription_chat(prescription_id):
    """Chat interface for a specific prescription"""
    prescription = Prescription.query.get_or_404(prescription_id)
    
    # Determine who to chat with based on role
    partner = None
    if current_user.role == 'doctor':
        # Doctor chats with patient or pharmacist
        partner_role = request.args.get('with', 'patient')
        if partner_role == 'patient':
            partner = prescription.patient.user
        elif partner_role == 'pharmacist':
            # Find pharmacist who requested modification
            from app.models.prescription_modification import PrescriptionModification
            mod = PrescriptionModification.query.filter_by(
                prescription_id=prescription_id
            ).order_by(PrescriptionModification.created_at.desc()).first()
            if mod:
                partner = mod.pharmacist.user
    
    elif current_user.role == 'pharmacist':
        # Pharmacist chats with prescribing doctor
        partner = prescription.doctor.user
    
    elif current_user.role == 'patient':
        # Patient chats with prescribing doctor
        partner = prescription.doctor.user
    
    return render_template('chat/index.html', 
                         prescription=prescription,
                         partner=partner)

