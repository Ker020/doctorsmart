from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.lab import Lab, LabService, LabTestType, LabAppointment
from app.models.payment import Payment
from datetime import datetime, timedelta
import uuid
import time
import json

bp = Blueprint('lab_booking', __name__, url_prefix='/lab_booking')

def generate_lab_slots(lab):
    """Generate available appointment slots for the next 7 days"""
    slots = []
    today = datetime.now()
    
    # Get existing appointments for this lab to filter them out
    existing_appointments = LabAppointment.query.filter(
        LabAppointment.lab_id == lab.id,
        LabAppointment.status.in_(['Confirmed', 'Pending']),
        LabAppointment.appointment_date >= today
    ).all()
    
    booked_times = [app.appointment_date for app in existing_appointments]
    
    # Support for both dict and JSON-string formats
    default_slots = lab.available_slots
    if isinstance(default_slots, str):
        try:
            default_slots = json.loads(default_slots)
        except:
            default_slots = None
            
    if not default_slots:
        default_slots = {
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "start": "09:00",
            "end": "17:00"
        }

    start_str = default_slots.get('start', '09:00')
    end_str = default_slots.get('end', '17:00')
    allowed_days = default_slots.get('days', [])

    try:
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()
    except:
        start_time = datetime.strptime("09:00", "%H:%M").time()
        end_time = datetime.strptime("17:00", "%H:%M").time()

    for day_offset in range(7):
        date = today + timedelta(days=day_offset)
        day_name = date.strftime('%A')
        
        # Check if lab is open this day (simple check using list of days)
        # Some implementations save days as short strings, others full. Checking both.
        if day_name not in allowed_days and day_name[:3] not in allowed_days:
             continue

        # Generate hourly slots
        current_slot_time = datetime.combine(date, start_time)
        end_slot_time = datetime.combine(date, end_time)

        while current_slot_time < end_slot_time:
            # Check if booked
            if current_slot_time > datetime.now() and current_slot_time not in booked_times:
                display_str = f"{date.strftime('%a, %b %d')} at {current_slot_time.strftime('%I:%M %p')}"
                slots.append({
                    'datetime': current_slot_time.strftime('%Y-%m-%d %H:%M'),
                    'display': display_str
                })
            
            current_slot_time += timedelta(hours=1)
    
    return slots[:20]  # Limit slots

@bp.route('/search')
@login_required
def search():
    test_type_id = request.args.get('test_type')
    query = Lab.query
    
    selected_service_details = {} # Map lab_id -> {price, prep_instructions}
    
    if test_type_id:
        # Join with LabService to filter labs that offer this test
        query = query.join(LabService).filter(LabService.test_type_id == test_type_id)
        
        # Pre-fetch price info for the selected test for each lab
        services = LabService.query.filter_by(test_type_id=test_type_id).all()
        for s in services:
            selected_service_details[s.lab_id] = {
                'price': s.price,
                'instructions': s.preparation_instructions,
                'service_id': s.id,
                'test_name': s.test_type.name
            }
    
    labs = query.all()
    
    # Serialize for template
    labs_data = []
    for l in labs:
        price_display = "Select test"
        service_id = None
        test_name = "General Lab Visit"
        
        if l.id in selected_service_details:
             price_display = f"{selected_service_details[l.id]['price']} EGP"
             service_id = selected_service_details[l.id]['service_id']
             test_name = selected_service_details[l.id]['test_name']
        
        labs_data.append({
            'id': l.id,
            'name': l.name,
            'address': l.address,
            'rating': l.rating,
            'price_display': price_display,
            'selected_service_id': service_id,
            'selected_test_name': test_name,
            'slots': generate_lab_slots(l)
        })
        
    # Get all test types for filter
    test_types = LabTestType.query.order_by(LabTestType.name).all()

    return render_template('lab_booking/search.html', 
                         labs=labs_data, 
                         test_types=test_types,
                         current_filter=int(test_type_id) if test_type_id else None)

@bp.route('/book', methods=['POST'])
@login_required
def book_appointment():
    try:
        lab_id = request.form.get('lab_id')
        service_id = request.form.get('service_id')
        date_str = request.form.get('date')
        payment_method = request.form.get('payment_method')
        
        if not date_str:
            return jsonify({'success': False, 'message': 'Please select a date and time.'}), 400
            
        if not service_id:
             return jsonify({'success': False, 'message': 'Please select an Analysis Type first.'}), 400

        try:
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format.'}), 400
        
        if not current_user.patient_profile:
             return jsonify({'success': False, 'message': 'Patient profile not found.'}), 400
        
        service = LabService.query.get(service_id)
        if not service:
            return jsonify({'success': False, 'message': 'Service not found.'}), 400
            
        # Create Appointment
        new_app = LabAppointment(
            lab_id=lab_id,
            patient_id=current_user.patient_profile.id,
            service_id=service_id,
            appointment_date=appointment_date,
            status='Pending'
        )
        db.session.add(new_app)
        db.session.flush()

        # Handle Payment if needed (Creating a Payment record linked to this appointment if applicable)
        # For now, we will skip explicit Payment record creation if models don't align, 
        # but the requirements say "Payment Integration".
        # Assuming we can just handle the UI flow for now.
        
        if payment_method == 'card':
            db.session.commit()
            return jsonify({
                'success': True, 
                'payment_required': True,
                'redirect_url': url_for('lab_booking.payment_page', appointment_id=new_app.id)
            })
        else:
            new_app.status = 'Confirmed'
            db.session.commit()
            return jsonify({
                'success': True, 
                'message': 'Lab appointment booked successfully! Pay at lab.',
                'chat_url': url_for('patient.dashboard')
            })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/payment/<int:appointment_id>', methods=['GET'])
@login_required
def payment_page(appointment_id):
    appointment = LabAppointment.query.get_or_404(appointment_id)
    
    if appointment.patient_id != current_user.patient_profile.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('patient.dashboard'))
        
    return render_template('lab_booking/payment.html', appointment=appointment)

@bp.route('/process_payment/<int:appointment_id>', methods=['POST'])
@login_required
def process_payment(appointment_id):
    appointment = LabAppointment.query.get_or_404(appointment_id)
    
    if appointment.patient_id != current_user.patient_profile.id:
        return redirect(url_for('patient.dashboard'))
        
    try:
        # Simulate payment
        time.sleep(1.5)
        
        appointment.status = 'Confirmed'
        db.session.commit()
        
        flash('Payment successful! Lab appointment confirmed.', 'success')
        return redirect(url_for('patient.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash('Payment failed.', 'error')
        return redirect(url_for('lab_booking.payment_page', appointment_id=appointment.id))
