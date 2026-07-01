from datetime import datetime
from app.extensions import db

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Prescription context (optional - for prescription-specific conversations)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=True)
    
    # Relationships
    prescription = db.relationship('Prescription', backref='chat_messages')

class QRToken(db.Model):
    __tablename__ = 'qr_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token_hash = db.Column(db.String(64), unique=True, nullable=False) # SHA-256
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    allowed_role = db.Column(db.String(20), nullable=False) # 'doctor' or 'pharmacist'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def is_valid(self):
        return datetime.utcnow() < self.expires_at
