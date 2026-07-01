from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from flask_login import login_required, current_user
from app.models.chat import QRToken
from app.models.medical_records import Prescription, MedicalReport
from app.models.prescription_modification import PrescriptionModification
from app.models.patient import Patient
from app.models.audit import AuditLog
from app.agents.pharmacist_agent import PharmacistAgent
from app.models.pharmacy import Pharmacist, Medication, PharmacySale, PharmacySaleItem
from app.extensions import db
from app.utils.decorators import role_required, prescription_access_required, grant_qr_access
from datetime import datetime

bp = Blueprint('pharmacist', __name__, url_prefix='/pharmacy')

@bp.route('/dashboard')
@login_required
@role_required('pharmacist')
def dashboard():
    """Pharmacist dashboard showing recent prescriptions and modification requests"""
    # Get pharmacist's modification requests
    modifications = PrescriptionModification.query.filter_by(
        pharmacist_id=current_user.pharmacist_profile.id
    ).order_by(PrescriptionModification.created_at.desc()).limit(10).all()
    
    # Get recently accessed prescriptions (from session or recent modifications)
    recent_prescriptions = []
    accessed_patient_ids = session.get('qr_accessed_patients', [])
    if accessed_patient_ids:
        recent_prescriptions = Prescription.query.filter(
            Prescription.patient_id.in_(accessed_patient_ids),
            Prescription.status == 'active'
        ).order_by(Prescription.created_at.desc()).limit(10).all()
    
    return render_template('pharmacist/dashboard.html', 
                         user=current_user,
                         modifications=modifications,
                         recent_prescriptions=recent_prescriptions)

@bp.route('/inventory')
@login_required
@role_required('pharmacist')
def inventory():
    """List all medications in inventory"""
    medications = Medication.query.order_by(Medication.name).all()
    return render_template('pharmacist/inventory.html', medications=medications)

@bp.route('/inventory/add', methods=['GET', 'POST'])
@login_required
@role_required('pharmacist')
def add_medication():
    """Add a new medication to inventory"""
    if request.method == 'POST':
        name = request.form.get('name')
        active_ingredient = request.form.get('active_ingredient')
        side_effects = request.form.get('side_effects')
        quantity = int(request.form.get('quantity', 0))
        price = float(request.form.get('price', 0.0))
        
        med = Medication(
            name=name,
            active_ingredient=active_ingredient,
            side_effects=side_effects,
            quantity=quantity,
            price=price
        )
        db.session.add(med)
        db.session.commit()
        flash(f'Medication {name} added successfully!', 'success')
        return redirect(url_for('pharmacist.inventory'))
    
    return render_template('pharmacist/add_medication.html')

@bp.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('pharmacist')
def edit_medication(id):
    """Edit an existing medication"""
    med = Medication.query.get_or_404(id)
    if request.method == 'POST':
        med.name = request.form.get('name')
        med.active_ingredient = request.form.get('active_ingredient')
        med.side_effects = request.form.get('side_effects')
        med.quantity = int(request.form.get('quantity', 0))
        med.price = float(request.form.get('price', 0.0))
        
        db.session.commit()
        flash(f'Medication {med.name} updated successfully!', 'success')
        return redirect(url_for('pharmacist.inventory'))
    
    return render_template('pharmacist/edit_medication.html', med=med)

@bp.route('/inventory/delete/<int:id>', methods=['POST'])
@login_required
@role_required('pharmacist')
def delete_medication(id):
    """Delete a medication from inventory"""
    med = Medication.query.get_or_404(id)
    db.session.delete(med)
    db.session.commit()
    flash(f'Medication deleted successfully!', 'success')
    return redirect(url_for('pharmacist.inventory'))

@bp.route('/inventory/alternatives/<int:id>')
@login_required
@role_required('pharmacist')
def view_alternatives(id):
    """Find medications with the same active ingredient"""
    med = Medication.query.get_or_404(id)
    alternatives = Medication.query.filter(
        Medication.active_ingredient == med.active_ingredient,
        Medication.id != med.id
    ).all()
    return render_template('pharmacist/alternatives.html', med=med, alternatives=alternatives)

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
@role_required('pharmacist')
def checkout():
    """Process a pharmacy sale with stock deduction"""
    if request.method == 'POST':
        # Simple checkout: one medication at a time for MVP
        med_id = request.form.get('medication_id')
        qty = int(request.form.get('quantity', 1))
        payment_method = request.form.get('payment_method') # Visa, Cash, InstaPay
        
        med = Medication.query.get(med_id)
        if not med or med.quantity < qty:
            flash('Insufficient stock or invalid medication.', 'error')
            return redirect(url_for('pharmacist.checkout'))
        
        # Deduct stock
        med.quantity -= qty
        
        # Record sale
        sale = PharmacySale(
            pharmacist_id=current_user.pharmacist_profile.id,
            total_amount=med.price * qty,
            payment_method=payment_method
        )
        db.session.add(sale)
        db.session.flush() # Get sale.id
        
        item = PharmacySaleItem(
            sale_id=sale.id,
            medication_id=med.id,
            quantity=qty,
            price_at_sale=med.price
        )
        db.session.add(item)
        
        # Log action
        AuditLog.log(
            user_id=current_user.id,
            action='pharmacy_sale_completed',
            resource_type='medication',
            resource_id=med.id,
            details={'quantity': qty, 'payment_method': payment_method}
        )
        
        db.session.commit()
        flash(f'Sale completed successfully via {payment_method}!', 'success')
        return redirect(url_for('pharmacist.inventory'))
    
    medications = Medication.query.filter(Medication.quantity > 0).all()
    return render_template('pharmacist/checkout.html', medications=medications)

# Original Routes follow...
@bp.route('/scan_qr_page')
@login_required
def scan_qr_page():
    if current_user.role != 'pharmacist':
        return redirect(url_for('auth.login'))
    return render_template('shared/scan_qr.html', post_url=url_for('pharmacist.scan_qr'))

@bp.route('/scan_qr', methods=['POST'])
@login_required
@role_required('pharmacist')
def scan_qr():
    token_str = request.form.get('token')
    token_entry = QRToken.query.filter_by(token_hash=token_str).first()
    if not token_entry:
        current_app.logger.warning(f"QR Scan (Pharm): Token {token_str[:10]}... not found.")
        flash('Invalid QR code', 'error')
        return redirect(url_for('pharmacist.dashboard'))
        
    if not token_entry.is_valid():
        current_app.logger.warning(f"QR Scan (Pharm): Token {token_str[:10]}... expired at {token_entry.expires_at}.")
        flash('Expired QR code', 'error')
        return redirect(url_for('pharmacist.dashboard'))
    if token_entry.allowed_role not in ['pharmacist', 'all']:
        flash('Unauthorized QR token', 'error')
        return redirect(url_for('pharmacist.dashboard'))
    grant_qr_access(token_entry.patient_id)
    AuditLog.log(user_id=current_user.id, action='qr_access_granted', resource_type='patient', resource_id=token_entry.patient_id, details={'token_id': token_entry.id})
    db.session.commit()
    return redirect(url_for('pharmacist.view_patient_prescriptions', patient_id=token_entry.patient_id))

@bp.route('/patient/<int:patient_id>/prescriptions')
@login_required
@role_required('pharmacist')
def view_patient_prescriptions(patient_id):
    qr_accessed_patients = session.get('qr_accessed_patients', [])
    if patient_id not in qr_accessed_patients:
        flash('QR code access required to view patient prescriptions.', 'error')
        return redirect(url_for('pharmacist.dashboard'))
    patient = Patient.query.get_or_404(patient_id)
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).order_by(Prescription.created_at.desc()).all()
    return render_template('pharmacist/view_patient_prescriptions.html', patient=patient, prescriptions=prescriptions)

@bp.route('/prescription/<int:prescription_id>')
@login_required
@role_required('pharmacist')
@prescription_access_required('prescription_id')
def view_prescription(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    modifications = PrescriptionModification.query.filter_by(prescription_id=prescription_id).order_by(PrescriptionModification.created_at.desc()).all()
    
    # Analyze prescription items vs inventory
    analysis = []
    
    for med in prescription.medications:
        # Search in inventory
        from app.models.medication import Medication
        inv_item = Medication.query.filter(Medication.name.like(f"%{med['name']}%")).first()
        
        item_analysis = {
            'prescribed_name': med['name'],
            'billing_name': med['name'], 
            'is_modified': False,
            'in_stock': inv_item and inv_item.quantity > 0,
            'stock_qty': inv_item.quantity if inv_item else 0,
            'price': inv_item.price if inv_item else 0.0,
            'inv_id': inv_item.id if inv_item else None,
            'active_ingredient': inv_item.active_ingredient if inv_item else None
        }
        analysis.append(item_analysis)
            
    return render_template('pharmacist/view_prescription.html', 
                         prescription=prescription, 
                         modifications=modifications,
                         analysis=analysis)

@bp.route('/prescription/<int:prescription_id>/request_modification', methods=['POST'])
@login_required
@role_required('pharmacist')
@prescription_access_required('prescription_id')
def request_modification(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    proposed_meds_str = request.form.get('proposed_medications')
    reason = request.form.get('reason')
    if not proposed_meds_str or not reason:
        flash('Please provide proposed medications and reason for modification.', 'error')
        return redirect(url_for('pharmacist.view_prescription', prescription_id=prescription_id))
    proposed_meds = []
    for line in proposed_meds_str.split('\n'):
        if '-' in line:
            parts = line.split('-')
            proposed_meds.append({'name': parts[0].strip(), 'dosage': parts[1].strip() if len(parts) > 1 else '', 'frequency': parts[2].strip() if len(parts) > 2 else ''})
    modification = PrescriptionModification(prescription_id=prescription_id, pharmacist_id=current_user.pharmacist_profile.id, original_medications=prescription.medications, proposed_medications=proposed_meds, reason=reason, status='pending', created_at=datetime.utcnow())
    db.session.add(modification)
    AuditLog.log(user_id=current_user.id, action='prescription_modification_requested', resource_type='prescription', resource_id=prescription_id, details={'modification_id': modification.id, 'reason': reason})
    db.session.commit()
    flash('Modification request submitted to doctor for approval.', 'success')
    return redirect(url_for('pharmacist.view_prescription', prescription_id=prescription_id))

@bp.route('/modifications')
@login_required
@role_required('pharmacist')
def view_modifications():
    modifications = PrescriptionModification.query.filter_by(pharmacist_id=current_user.pharmacist_profile.id).order_by(PrescriptionModification.created_at.desc()).all()
    return render_template('pharmacist/modifications.html', modifications=modifications)

@bp.route('/check_drug', methods=['POST'])
@login_required
@role_required('pharmacist')
def check_drug():
    data = request.get_json()
    drug_name = data.get('drug_name')
    alternatives = PharmacistAgent.suggest_alternatives(drug_name)
    return jsonify({'alternatives': alternatives})

