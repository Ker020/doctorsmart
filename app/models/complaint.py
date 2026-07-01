from app.extensions import db
from datetime import datetime

class Complaint(db.Model):
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_role = db.Column(db.String(50))  # 'doctor', 'lab', 'pharmacist'
    target_id = db.Column(db.Integer)  # Optional: specific doctor/lab/pharmacist ID
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    admin_response = db.Column(db.Text)  # Admin's response to the complaint
    status = db.Column(db.String(50), default='Pending')  # Pending, Responded, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)  # When admin responded

    # Relationship
    user = db.relationship('User', backref=db.backref('complaints', lazy=True))

    def __repr__(self):
        return f'<Complaint {self.subject} by User {self.user_id}>'
