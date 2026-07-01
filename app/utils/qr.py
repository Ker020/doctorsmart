import hashlib
import qrcode
import os
from datetime import datetime, timedelta
from flask import current_app

def generate_qr_token(patient_id, role, expiry_minutes=30):
    """
    Generates a secure SHA-256 token for QR access.
    Token includes patient_id, allowed_role, timestamp and a secret salt.
    """
    timestamp = datetime.utcnow().isoformat()
    raw_data = f"{patient_id}-{role}-{timestamp}-{current_app.config['SECRET_KEY']}"
    token_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    # In a real system, you'd store this token in the DB with an expiration time.
    # For this implementation, we will return the hash + metadata to be stored by the caller.
    return token_hash

def create_qr_image(data, filename):
    """
    Creates a QR code image file.
    data: The content of the QR code (e.g., URL or Token)
    filename: valid filename (e.g. 'token_123.png')
    Returns: relative path to the image
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)
            # Ensure the directory has correct permissions if we just created it
            os.chmod(upload_folder, 0o775)
            
        file_path = os.path.join(upload_folder, filename)
        
        # Save the image
        img.save(file_path)
        
        # Ensure the file has correct permissions for the web server group
        try:
            os.chmod(file_path, 0o664)
        except Exception as e:
            logger.warning(f"Could not set permissions on {file_path}: {e}")

        # Return path relative to static folder for HTML usage
        return f"uploads/{filename}"
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        # If it fails (e.g., permission error even after chmod), 
        # check if the file already exists as a fallback
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return f"uploads/{filename}"
        return None
