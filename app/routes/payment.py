from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.services.payment_service import PaymentService
from app.models.payment import Payment
from app.models.appointment import Appointment

bp = Blueprint('payment', __name__, url_prefix='/payment')

@bp.route('/create', methods=['POST'])
@login_required
def create_payment():
    """
    Create a new payment for an appointment
    """
    data = request.get_json()
    
    appointment_id = data.get('appointment_id')
    payment_method = data.get('payment_method', 'card')
    
    # Get appointment details
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'success': False, 'error': 'Appointment not found'}), 404
    
    # Verify user owns this appointment
    if current_user.role == 'patient':
        if appointment.patient_id != current_user.patient_profile.id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    # Get doctor price
    amount = appointment.doctor.price
    
    # Create payment
    result = PaymentService.create_payment(
        appointment_id=appointment_id,
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        amount=amount,
        payment_method=payment_method
    )
    
    return jsonify(result)

@bp.route('/process', methods=['POST'])
@login_required
def process_payment():
    """
    Process a pending payment
    """
    data = request.get_json()
    payment_id = data.get('payment_id')
    payment_details = data.get('payment_details', {})
    
    result = PaymentService.process_payment(payment_id, payment_details)
    return jsonify(result)

@bp.route('/history')
@login_required
def payment_history():
    """
    Get payment history for current user
    """
    if current_user.role != 'patient':
        return jsonify({'success': False, 'error': 'Only patients can view payment history'}), 403
    
    history = PaymentService.get_payment_history(current_user.patient_profile.id)
    return jsonify({'success': True, 'payments': history})

@bp.route('/refund/<int:payment_id>', methods=['POST'])
@login_required
def refund_payment(payment_id):
    """
    Refund a payment (admin or doctor only)
    """
    if current_user.role not in ['admin', 'doctor']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    reason = data.get('reason', 'Requested by user')
    
    result = PaymentService.refund_payment(payment_id, reason)
    return jsonify(result)
