import os
from pdf_reader import extract_text_from_pdf
from ocr_reader import extract_text_from_image

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)

        # لو PDF صورة مش text
        if len(text.strip()) < 20:
            print("PDF appears scanned. Running OCR...")
            text = extract_text_from_image(file_path)

        return text

    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)

    else:
        raise ValueError("Unsupported file format")
