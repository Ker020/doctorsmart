from app.extensions import db
from datetime import datetime

class MedicalReport(db.Model):
    __tablename__ = 'medical_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    report_type = db.Column(db.String(50))  # 'diagnosis', 'consultation', 'follow-up'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Deletion Request Logic
    deletion_requested = db.Column(db.Boolean, default=False)
    deletion_reason = db.Column(db.Text)
    
    # Relationships
    patient = db.relationship('Patient', backref='medical_reports')
    doctor = db.relationship('Doctor', backref='medical_reports')
    
    def __repr__(self):
        return f'<MedicalReport {self.title}>'


class LabTest(db.Model):
    __tablename__ = 'lab_tests'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    test_name = db.Column(db.String(200), nullable=False)
    test_type = db.Column(db.String(100))  # 'blood', 'urine', 'xray', 'mri', 'ct'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'cancelled'
    results = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    ordered_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    # Relationships
    patient = db.relationship('Patient', backref='lab_tests')
    doctor = db.relationship('Doctor', backref='lab_tests')
    
    def __repr__(self):
        return f'<LabTest {self.test_name}>'


class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    medications = db.Column(db.JSON)  # List of {name, dosage, frequency, duration}
    instructions = db.Column(db.Text)
    diagnosis = db.Column(db.String(200))
    valid_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # 'active', 'expired', 'filled'
    
    # Relationships
    patient = db.relationship('Patient', backref='prescriptions')
    doctor = db.relationship('Doctor', backref='prescriptions')
    
    def __repr__(self):
        return f'<Prescription {self.id} for Patient {self.patient_id}>'


class FollowUpAppointment(db.Model):
    __tablename__ = 'follow_up_appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    original_appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    scheduled_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # 'scheduled', 'completed', 'cancelled'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = db.relationship('Patient', backref='follow_ups')
    doctor = db.relationship('Doctor', backref='follow_ups')
    
    def __repr__(self):
        return f'<FollowUp {self.id}>'


class VitalSigns(db.Model):
    __tablename__ = 'vital_signs'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    respiratory_rate = db.Column(db.Integer)
    oxygen_saturation = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    bmi = db.Column(db.Float)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relationships
    patient = db.relationship('Patient', backref='vital_signs')
    
    def __repr__(self):
        return f'<VitalSigns for Patient {self.patient_id}>'
