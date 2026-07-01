import os
import json
import markdown
from flask import Flask
from .config import Config
from .extensions import init_extensions, db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize Flask extensions
    init_extensions(app)

    @app.template_filter('from_json')
    def from_json_filter(s):
        if not s: return None
        try:
            return json.loads(s)
        except:
            return None

    @app.template_filter('markdown')
    def markdown_filter(text):
        if not text:
            return ""
        return markdown.markdown(text, extensions=['extra', 'nl2br'])

    # Register Blueprints
    from .routes import auth, patient, doctor, pharmacist, chat, admin, booking, payment, medical, lab, lab_booking
    app.register_blueprint(auth.bp)
    app.register_blueprint(patient.bp)
    app.register_blueprint(doctor.bp)
    app.register_blueprint(pharmacist.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(booking.bp)
    app.register_blueprint(payment.bp)
    app.register_blueprint(medical.bp)
    app.register_blueprint(lab.bp)
    app.register_blueprint(lab_booking.bp)

    from .routes import ai
    app.register_blueprint(ai.bp)

    # Create Database Tables
    with app.app_context():
        # Import models so SQLAlchemy knows about them before create_all
        from .models import user, patient, doctor, pharmacy, chat, payment, medical_records, rating, complaint, lab
        db.create_all()

    return app
