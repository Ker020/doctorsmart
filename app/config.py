import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bcb1a40d98030f0b18c84816e28108e903f1228b4f1aa6c1e02107afaca89b21'
    
    # Database Configuration (MariaDB)
    # Ensure you have created the database 'smart_healthcare' in MariaDB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "mysql+pymysql://root:Ahmed%403300805@localhost/smart_healthcare"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload setup

    # AI Configuration
    LLM_API_URL = "http://127.0.0.1:11434/v1/chat/completions"
    LLM_MODEL = "qwen2.5:1.5b"
    LLM_MODEL_NAME = LLM_MODEL  # Alias for compatibility
    LLM_TIMEOUT = int(os.environ.get("LLM_TIMEOUT", "600"))

    # Google Maps Configuration
    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    GOOGLE_PLACES_KEY = os.environ.get("GOOGLE_PLACES_KEY", GOOGLE_MAPS_API_KEY)
