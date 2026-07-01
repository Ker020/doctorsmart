from app.extensions import db
from datetime import datetime

class PrescriptionModification(db.Model):
    """
    Tracks pharmacist-requested changes to prescriptions.
    Doctor must approve/reject these modifications.
    """
    __tablename__ = 'prescription_modifications'
    
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=False)
    pharmacist_id = db.Column(db.Integer, db.ForeignKey('pharmacists.id'), nullable=False)
    
    # Medication snapshots
    original_medications = db.Column(db.JSON)  # Original prescription medications
    proposed_medications = db.Column(db.JSON)  # Pharmacist's proposed changes
    
    # Request details
    reason = db.Column(db.Text, nullable=False)  # Why the change is needed
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    
    # Doctor's response
    doctor_response = db.Column(db.Text)  # Doctor's notes on approval/rejection
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    
    # Relationships
    prescription = db.relationship('Prescription', backref='modification_requests')
    pharmacist = db.relationship('Pharmacist', backref='modification_requests')
    
    def __repr__(self):
        return f'<PrescriptionModification {self.id} - {self.status}>'
    
    def approve(self, doctor_response=None):
        """Approve the modification and update the prescription"""
        self.status = 'approved'
        self.doctor_response = doctor_response
        self.reviewed_at = datetime.utcnow()
        
        # Update the prescription with proposed medications
        self.prescription.medications = self.proposed_medications
        
    def reject(self, doctor_response=None):
        """Reject the modification"""
        self.status = 'rejected'
        self.doctor_response = doctor_response
        self.reviewed_at = datetime.utcnow()
