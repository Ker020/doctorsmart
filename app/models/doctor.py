from app.extensions import db

class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, default=0.0)
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(255), default="default_doctor.png")
    rating = db.Column(db.Float, default=4.5)
    total_patients = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    # Storing complex structures as JSON for MVP simplicity (MariaDB supports JSON)
    locations = db.Column(db.JSON) # List of {"name": "Clinic A", "address": "..."}
    available_slots = db.Column(db.JSON) # List of {"day": "Monday", "times": ["10:00", "11:00"]}

    # Relationships
    user = db.relationship("User", back_populates="doctor_profile")

    def __repr__(self):
        return f"<Doctor {self.specialty}>"
