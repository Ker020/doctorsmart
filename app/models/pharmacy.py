from app.extensions import db
from datetime import datetime

class Pharmacist(db.Model):
    __tablename__ = "pharmacists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    pharmacy_name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="pharmacist_profile")

    def __repr__(self):
        return f"<Pharmacist {self.pharmacy_name}>"

class Medication(db.Model):
    __tablename__ = "medications"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # Brand Name
    active_ingredient = db.Column(db.String(100), nullable=False) # Generic Name
    side_effects = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Medication {self.name}>"

class PharmacySale(db.Model):
    __tablename__ = "pharmacy_sales"
    id = db.Column(db.Integer, primary_key=True)
    pharmacist_id = db.Column(db.Integer, db.ForeignKey("pharmacists.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False) # Visa, Cash, InstaPay
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    pharmacist = db.relationship("Pharmacist", backref="sales")
    patient = db.relationship("Patient", backref="pharmacy_purchases")

    def __repr__(self):
        return f"<PharmacySale {self.id} - {self.payment_method}>"

class PharmacySaleItem(db.Model):
    __tablename__ = "pharmacy_sale_items"
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("pharmacy_sales.id"))
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.id"))
    quantity = db.Column(db.Integer, nullable=False)
    price_at_sale = db.Column(db.Float, nullable=False)

    sale = db.relationship("PharmacySale", backref="items")
    medication = db.relationship("Medication", backref="sale_instances")
