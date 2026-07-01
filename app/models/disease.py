from app.extensions import db
from datetime import datetime

class Disease(db.Model):
    __tablename__ = 'diseases'
    
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(200), nullable=False)
    name_ar = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), unique=True) # ICD-10 or similar
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Disease {self.name_en}>'
