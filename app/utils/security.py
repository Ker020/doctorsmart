import hashlib
import qrcode
import os
from datetime import datetime, timedelta
from flask import current_app

def generate_qr_token(patient_id, role):
    """
    Generates a secure SHA-256 token for QR codes.
    Token format: patient_id-role-timestamp
    """
    raw_string = f"{patient_id}-{role}-{datetime.utcnow().isoformat()}"
    token_hash = hashlib.sha256(raw_string.encode()).hexdigest()
    return token_hash

def create_qr_image(token_hash):
    """
    Creates a QR code image from the token hash and saves it.
    Returns the relative path to the image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # The data in the QR code is the URL to the verify endpoint
    # For now we just put the token
    qr.add_data(token_hash)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"{token_hash}.png"
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    img.save(save_path)
    
    return filename
