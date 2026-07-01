import os
import sys
from typing import Dict, Any, Optional

# Add the utils directory to python path so sub-modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
engine_dir = os.path.join(current_dir, "..", "utils", "analysis_engine")
if engine_dir not in sys.path:
    sys.path.append(engine_dir)

try:
    from app.utils.analysis_engine.analyzer import CBCAnalyzer
    from app.utils.analysis_engine.pdf_reader import extract_text_from_pdf
    from app.utils.analysis_engine.ocr_reader import extract_text_from_image
except ImportError:
    # Fallback or logging if engine files are not yet copied
    CBCAnalyzer = None

class AnalysisService:
    def __init__(self):
        self.analyzer = CBCAnalyzer() if CBCAnalyzer else None

    def analyze_lab_report(self, file_path: str, patient_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze a lab report file (PDF or Image) and return the results.
        
        Args:
            file_path: Absolute path to the file
            patient_data: Optional dictionary with "age", "gender", "pregnant"
            
        Returns:
            Dictionary containing the analysis result
        """
        if not self.analyzer:
            return {"error": "Analysis engine not initialized"}

        if not os.path.exists(file_path):
            return {"error": "File not found"}
            
        # Extract text based on file type
        try:
            text = ""
            if file_path.lower().endswith(".pdf"):
                # We need to ensure dependencies are installed for this
                text = extract_text_from_pdf(file_path)
            elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                text = extract_text_from_image(file_path)
            else:
                return {"error": "Unsupported file format. Please upload PDF or Image."}
                
            if not text.strip():
                return {"error": "Could not extract text from file. Please ensure the image/pdf is clear."}

            # Prepare patient parameters
            age = patient_data.get("age") if patient_data else None
            gender = patient_data.get("gender") if patient_data else None
            pregnant = patient_data.get("pregnant", False) if patient_data else False

            # Run Analysis
            result = self.analyzer.analyze(text, age=age, gender=gender, pregnant=pregnant)
            
            # Serialize result to dict using built-in method
            if hasattr(result, 'to_dict'):
                analysis_data = result.to_dict()
            else:
                # Fallback for unexpected return types
                analysis_data = result

            return {
                "success": True,
                "data": analysis_data
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": f"Analysis failed: {str(e)}"}
