from app.extensions import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    medical_id = db.Column(db.String(36), unique=True, nullable=False) # UUID
    dob = db.Column(db.Date, nullable=False)
    blood_type = db.Column(db.String(5))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    chronic_diseases = db.Column(db.Text)
    
    # MOH Fields (Existing in database)
    national_id = db.Column(db.String(14), unique=True)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    gender = db.Column(db.String(10))
    governorate = db.Column(db.String(50))
    
    # Relationships
    user = db.relationship("User", back_populates="patient_profile")
    
    def __repr__(self):
        return f"<Patient {self.medical_id}>"
