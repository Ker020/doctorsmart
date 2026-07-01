from app.extensions import db
from datetime import datetime

class AuditLog(db.Model):
    """
    Audit trail for sensitive operations in the system.
    Tracks who did what, when, and on which resource.
    """
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Action details
    action = db.Column(db.String(100), nullable=False)  # e.g., 'prescription_modified', 'record_deleted'
    resource_type = db.Column(db.String(50))  # e.g., 'prescription', 'medical_report'
    resource_id = db.Column(db.Integer)  # ID of the affected resource
    
    # Additional context
    details = db.Column(db.JSON)  # Any additional details about the action
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='audit_logs')
    
    def __repr__(self):
        return f'<AuditLog {self.action} by User {self.user_id}>'
    
    @staticmethod
    def log(user_id, action, resource_type=None, resource_id=None, details=None, ip_address=None):
        """
        Convenience method to create audit log entries.
        
        Usage:
            AuditLog.log(
                user_id=current_user.id,
                action='prescription_modified',
                resource_type='prescription',
                resource_id=prescription.id,
                details={'changes': 'Updated medications'}
            )
        """
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address
        )
        db.session.add(log_entry)
        return log_entry
