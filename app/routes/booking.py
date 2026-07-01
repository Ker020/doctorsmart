from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.payment import Payment
from datetime import datetime, timedelta
import json
import uuid
import time

bp = Blueprint('booking', __name__, url_prefix='/booking')

def generate_appointment_slots(doctor):
    """Generate available appointment slots for the next 7 days"""
    slots = []
    today = datetime.now()
    
    # Get existing appointments for this doctor to filter them out
    existing_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.status.in_(['confirmed', 'pending']),
        Appointment.appointment_date >= today
    ).all()
    
    booked_times = [app.appointment_date for app in existing_appointments]
    
    # Default slots if none defined (Mon-Sun, 10am-4pm) for MVP
    default_slots = doctor.available_slots or [
        {"day": d, "times": ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]}
        for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ]

    for day_offset in range(7):
        date = today + timedelta(days=day_offset)
        day_name = date.strftime('%A')
        
        # Find slots for this day
        for slot_day in default_slots:
            if slot_day.get('day') == day_name:
                for time_str in slot_day.get('times', []):
                    # Combine date and time
                    datetime_str = f"{date.strftime('%Y-%m-%d')} {time_str}"
                    # Skip past slots
                    slot_dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                    
                    if slot_dt > datetime.now() and slot_dt not in booked_times:
                        # 12h format display: e.g. "Sun, Dec 28 at 10:00 AM"
                        display_str = f"{date.strftime('%a, %b %d')} at {slot_dt.strftime('%I:%M %p')}"
                        
                        slots.append({
                            'datetime': datetime_str,
                            'display': display_str
                        })
    
    return slots[:15]  # Return first 15 slots

@bp.route('/search')
@login_required
def search():
    specialty = request.args.get('specialty')
    query = Doctor.query
    if specialty:
        query = query.filter(Doctor.specialty.ilike(f'%{specialty}%'))
    
    doctors = query.all()
    
    # Serialize for template with enhanced data
    doctors_data = []
    for d in doctors:
        doctors_data.append({
            'id': d.id,
            'name': d.user.name,
            'specialty': d.specialty,
            'price': d.price,
            'bio': d.bio,
            'profile_image': d.profile_image,
            'rating': d.rating,
            'total_patients': d.total_patients,
            'location': d.locations[0]['address'] if d.locations else 'N/A',
            'slots': generate_appointment_slots(d)
        })
        
    # Get all distinct specialties for the filter dropdown
    try:
        specialties_query = db.session.query(Doctor.specialty).distinct().order_by(Doctor.specialty).all()
        # Filter out None strings if any, and extract from tuple
        specialties = [s[0] for s in specialties_query if s[0]]
    except Exception as e:
        print(f"Error fetching specialties: {e}")
        specialties = []
        
    return render_template('booking/search.html', doctors=doctors_data, specialties=specialties)

@bp.route('/doctor/<int:doctor_id>')
@login_required
def doctor_profile(doctor_id):
    """View doctor profile with all ratings"""
    doctor = Doctor.query.get_or_404(doctor_id)
    
    # Get all ratings for this doctor
    from app.models.rating import Rating
    ratings = Rating.query.filter_by(doctor_id=doctor_id)\
                          .order_by(Rating.created_at.desc()).all()
    
    # Check if current user is a patient
    is_patient = current_user.role == 'patient'
    
    return render_template('booking/doctor_profile.html', 
                         doctor=doctor, 
                         ratings=ratings,
                         is_patient=is_patient)

@bp.route('/book', methods=['POST'])
@login_required
def book_appointment():
    try:
        doctor_id = request.form.get('doctor_id')
        date_str = request.form.get('date')  # e.g. "2024-12-25 10:00"
        payment_method = request.form.get('payment_method')
        
        if not date_str:
            return jsonify({'success': False, 'message': 'Please select a date and time.'}), 400

        # Simple validation
        try:
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format.'}), 400
        
        # Check if patient profile exists
        if not current_user.patient_profile:
             return jsonify({'success': False, 'message': 'Patient profile not found.'}), 400
        
        # Determine status based on payment method
        # If card, status remains 'pending' until paid.
        # If cash, status is 'confirmed' (or 'pending' awaiting doctor approval, let's say confirmed for MVP)
        initial_status = 'pending' 
        
        new_app = Appointment(
            doctor_id=doctor_id,
            patient_id=current_user.patient_profile.id,
            appointment_date=appointment_date,
            status=initial_status,
            type='consultation'
        )
        db.session.add(new_app)
        db.session.flush() # Get ID
        
        # Create Payment Record
        doctor = Doctor.query.get(doctor_id)
        new_payment = Payment(
            appointment_id=new_app.id,
            patient_id=current_user.patient_profile.id,
            doctor_id=doctor_id,
            amount=doctor.price,
            payment_method=payment_method,
            status='pending'
        )
        db.session.add(new_payment)
        db.session.commit()
        
        if payment_method == 'card':
            return jsonify({
                'success': True, 
                'payment_required': True,
                'redirect_url': url_for('booking.payment_page', appointment_id=new_app.id)
            })
        else:
            # For cash, confirm immediately
            new_app.status = 'confirmed'
            db.session.commit()
            return jsonify({
                'success': True, 
                'message': 'Appointment booked successfully! Pay at clinic.',
                'chat_url': url_for('chat.index', partner_id=doctor.user_id)
            })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/payment/<int:appointment_id>', methods=['GET'])
@login_required
def payment_page(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Security check
    if appointment.patient_id != current_user.patient_profile.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('patient.dashboard'))
        
    if appointment.status == 'confirmed':
        flash('Appointment already paid/confirmed', 'info')
        return redirect(url_for('patient.dashboard'))

    return render_template('booking/payment.html', appointment=appointment)

@bp.route('/process_payment/<int:appointment_id>', methods=['POST'])
@login_required
def process_payment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.patient_id != current_user.patient_profile.id:
        return redirect(url_for('patient.dashboard'))
    
    try:
        # Simulate payment processing
        time.sleep(1.5) 
        
        # Update records
        payment = Payment.query.filter_by(appointment_id=appointment.id).first()
        if payment:
            payment.status = 'completed'
            payment.transaction_id = f"TRX-{uuid.uuid4().hex[:12].upper()}"
            
        appointment.status = 'confirmed'
        db.session.commit()
        
        flash('Payment successful! Your appointment is confirmed.', 'success')
        return redirect(url_for('chat.index', partner_id=appointment.doctor.user_id))
        
    except Exception as e:
        db.session.rollback()
        flash('Payment failed. Please try again.', 'danger')
        return redirect(url_for('booking.payment_page', appointment_id=appointment.id))
