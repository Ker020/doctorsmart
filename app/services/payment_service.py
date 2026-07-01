"""
Payment Service
Handles payment processing and integration
"""
import uuid
from datetime import datetime
from app.extensions import db
from app.models.payment import Payment

class PaymentService:
    
    @staticmethod
    def create_payment(appointment_id, patient_id, doctor_id, amount, payment_method='card'):
        """
        Create a new payment record
        """
        try:
            transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            
            payment = Payment(
                appointment_id=appointment_id,
                patient_id=patient_id,
                doctor_id=doctor_id,
                amount=amount,
                payment_method=payment_method,
                status='pending',
                transaction_id=transaction_id,
                payment_date=datetime.utcnow()
            )
            
            db.session.add(payment)
            db.session.commit()
            
            return {
                'success': True,
                'transaction_id': transaction_id,
                'payment_id': payment.id
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def process_payment(payment_id, payment_details=None):
        """
        Process payment (mock implementation for MVP)
        In production, integrate with real payment gateway
        """
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return {'success': False, 'error': 'Payment not found'}
            
            # Mock payment processing
            # In production: integrate with Stripe, PayPal, Fawry, etc.
            payment.status = 'completed'
            payment.notes = 'Payment processed successfully'
            
            # Update appointment status
            if payment.appointment:
                payment.appointment.status = 'confirmed'
            
            db.session.commit()
            
            return {
                'success': True,
                'transaction_id': payment.transaction_id,
                'status': 'completed'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_payment_history(patient_id):
        """
        Get payment history for a patient
        """
        payments = Payment.query.filter_by(patient_id=patient_id)\
                                .order_by(Payment.payment_date.desc())\
                                .all()
        
        return [{
            'id': p.id,
            'transaction_id': p.transaction_id,
            'amount': p.amount,
            'status': p.status,
            'payment_method': p.payment_method,
            'payment_date': p.payment_date.strftime('%Y-%m-%d %H:%M'),
            'doctor_name': p.doctor.user.name if p.doctor else 'N/A'
        } for p in payments]
    
    @staticmethod
    def refund_payment(payment_id, reason=''):
        """
        Refund a payment
        """
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return {'success': False, 'error': 'Payment not found'}
            
            if payment.status != 'completed':
                return {'success': False, 'error': 'Can only refund completed payments'}
            
            payment.status = 'refunded'
            payment.notes = f'Refunded: {reason}'
            
            # Update appointment status
            if payment.appointment:
                payment.appointment.status = 'cancelled'
            
            db.session.commit()
            
            return {
                'success': True,
                'transaction_id': payment.transaction_id,
                'status': 'refunded'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
