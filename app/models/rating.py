from app.extensions import db
from datetime import datetime

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), unique=True, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    stars = db.Column(db.Integer, nullable=False) # 1-5
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    appointment = db.relationship('Appointment', backref=db.backref('rating', uselist=False))
    doctor = db.relationship('Doctor', backref='ratings_received')
    patient = db.relationship('Patient', backref='ratings_given')

    def __repr__(self):
        return f'<Rating {self.stars} stars for Doctor {self.doctor_id}>'
