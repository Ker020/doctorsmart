from app.extensions import db
from datetime import datetime

class Lab(db.Model):
    __tablename__ = "labs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255))
    license_number = db.Column(db.String(100))
    rating = db.Column(db.Float, default=4.5)
    available_slots = db.Column(db.JSON) # e.g. {"days": ["Mon", "Tue"], "start": "09:00", "end": "17:00"} or list of slots
    
    # Relationships
    user = db.relationship("User", back_populates="lab_profile")
    services = db.relationship("LabService", backref="lab", lazy=True)
    appointments = db.relationship("LabAppointment", backref="lab", lazy=True)

    def __repr__(self):
        return f"<Lab {self.name}>"

class LabTestType(db.Model):
    __tablename__ = "lab_test_types"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    category = db.Column(db.String(100)) # e.g. "Blood Work", "Imaging", "Pathology"
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<LabTestType {self.name}>"

class LabService(db.Model):
    __tablename__ = "lab_services"

    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id"), nullable=False)
    test_type_id = db.Column(db.Integer, db.ForeignKey("lab_test_types.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    preparation_instructions = db.Column(db.Text) # Fasting hours etc.
    turnaround_time = db.Column(db.String(100)) # e.g. "24 Hours"
    description = db.Column(db.Text) # Lab specific description

    # Relationships
    test_type = db.relationship("LabTestType", backref="offered_by")

    def __repr__(self):
        return f"<LabService {self.test_type.name} at {self.lab.name}>"

class LabAppointment(db.Model):
    __tablename__ = "lab_appointments"
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("lab_services.id"), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="Pending") # Pending, Confirmed, Completed, Cancelled
    result_file = db.Column(db.String(255)) # Path to uploaded report
    result_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    patient = db.relationship("Patient", backref="lab_appointments")
    service = db.relationship("LabService")
    
    def __repr__(self):
        return f"<LabAppointment {self.id} Status: {self.status}>"
