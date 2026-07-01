from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'patient', 'doctor', 'pharmacist', 'admin', 'lab'
    profile_image = db.Column(db.String(255), default='default_avatar.png')
    is_active = db.Column(db.Boolean, default=True)  # For account blocking/activation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Profile Relationships for robust cascade deletes
    doctor_profile = db.relationship('Doctor', back_populates='user', uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    patient_profile = db.relationship('Patient', back_populates='user', uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    pharmacist_profile = db.relationship('Pharmacist', back_populates='user', uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    lab_profile = db.relationship('Lab', back_populates='user', uselist=False, cascade="all, delete-orphan", passive_deletes=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name} - {self.role}>'
