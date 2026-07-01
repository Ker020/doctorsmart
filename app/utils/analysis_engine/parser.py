import re
from typing import Dict, Optional, Tuple, List
from normalizer import normalize_test_name



class LabReportParser:
    """
    Advanced parser for extracting lab values from text.
    Handles multiple formats, OCR noise, and various lab report styles.
    """
    
    # Pattern 1: Standard format with colons/equals
    # Example: "Hemoglobin: 12.5" or "HB = 12.5"
    PATTERN_STANDARD = r'([A-Za-z\s\(\)\/]+)[\s]*[\:\-\=]\s*([\d\.]+)'
    
    # Pattern 2: Value after test name with optional unit
    # Example: "Hemoglobin 12.5 g/dL"
    PATTERN_WITH_UNIT = r'([A-Za-z\s\(\)\/]+)\s+([\d\.]+)\s*(?:[a-zA-Z\/\%]+)?'
    
    # Pattern 3: Scientific notation or ranges
    # Example: "WBC 4.5 x10^3/uL" or "4.5x10^3"
    PATTERN_SCIENTIFIC = r'([A-Za-z\s\(\)\/]+)[\s]*[\:\-\=]?\s*([\d\.]+)\s*[xX×]\s*10\s*[\^\*]?\s*[\d]+'
    
    # Pattern 4: Reference range extraction
    # Example: "Reference: 13.0 - 17.0" or "Ref: 13-17" or "(13.0-17.0)"
    PATTERN_REFERENCE = r'(?:Reference|Ref|Normal)[\s\:]*\(?([\d\.]+)\s*[\-–—]\s*([\d\.]+)\)?'
    
    @classmethod
    def extract_patient_info(cls, text: str) -> Dict[str, Optional[str]]:
        """
        Extract patient demographic information from lab report.
        
        Returns:
            Dictionary with patient_name, age, gender, date, lab_name
        """
        info = {
            "patient_name": None,
            "age": None,
            "gender": None,
            "date": None,
            "lab_name": None
        }
        
        # Extract patient name
        name_patterns = [
            r'Patient\s+Name[\s\:]+([A-Za-z\s]+?)(?:\n|Age)',
            r'Name[\s\:]+([A-Za-z\s]+?)(?:\n|Age)',
        ]
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info["patient_name"] = match.group(1).strip()
                break
        
        # Extract age
        age_patterns = [
            r'Age[\s\:]+(\d+)',
            r'Age[\s\:]+(\d+)\s*(?:Years|Yrs|Y)',
        ]
        for pattern in age_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info["age"] = match.group(1).strip()
                break
        
        # Extract gender
        gender_patterns = [
            r'Gender[\s\:]+([A-Za-z]+)',
            r'Sex[\s\:]+([A-Za-z]+)',
        ]
        for pattern in gender_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                gender = match.group(1).strip().lower()
                if gender in ['male', 'm']:
                    info["gender"] = "male"
                elif gender in ['female', 'f']:
                    info["gender"] = "female"
                break
        
        # Extract date
        date_patterns = [
            r'Date[\s\:]+(\d{1,2}[\-\/]\d{1,2}[\-\/]\d{2,4})',
            r'(\d{1,2}[\-\/]\d{1,2}[\-\/]\d{2,4})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                info["date"] = match.group(1).strip()
                break
        
        # Extract lab name (usually at the top)
        lines = text.split('\n')
        if lines:
            first_line = lines[0].strip()
            # If first line looks like a lab name (all caps, contains "lab" or "laboratory")
            if re.search(r'LAB(?:ORATORY)?', first_line, re.IGNORECASE) or first_line.isupper():
                info["lab_name"] = first_line
        
        return info
    
    @classmethod
    def extract_test_values(cls, text: str) -> Dict[str, float]:
        """
        Extract all test values from lab report text.
        Handles multiple formats and OCR errors.
        
        Returns:
            Dictionary mapping standardized test names to values
        """
        values = {}
        
        # Try all patterns
        patterns = [
            cls.PATTERN_SCIENTIFIC,  # Try scientific notation first
            cls.PATTERN_STANDARD,
            cls.PATTERN_WITH_UNIT,
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            for match in matches:
                if len(match) >= 2:
                    raw_name, raw_value = match[0], match[1]
                    
                    # Normalize the test name
                    test_name = normalize_test_name(raw_name.strip())
                    
                    if not test_name:
                        continue
                    
                    # Parse the value
                    try:
                        value = float(raw_value)
                        
                        # Skip unrealistic values (likely OCR errors)
                        if cls._is_realistic_value(test_name, value):
                            values[test_name] = value
                    except (ValueError, TypeError):
                        continue
        
        return values
    
    @classmethod
    def extract_reference_ranges(cls, text: str, test_name: str) -> Optional[Tuple[float, float]]:
        """
        Extract reference range for a specific test from the text.
        
        Args:
            text: Lab report text
            test_name: Standardized test name
            
        Returns:
            Tuple of (min, max) or None if not found
        """
        # Find the line containing the test name
        lines = text.split('\n')
        
        for line in lines:
            # Check if this line contains our test
            if normalize_test_name(line) == test_name:
                # Look for reference range in this line
                match = re.search(cls.PATTERN_REFERENCE, line, re.IGNORECASE)
                if match:
                    try:
                        min_val = float(match.group(1))
                        max_val = float(match.group(2))
                        return (min_val, max_val)
                    except (ValueError, TypeError):
                        continue
        
        return None
    
    @staticmethod
    def _is_realistic_value(test_name: str, value: float) -> bool:
        """
        Check if a value is realistic for the given test.
        Helps filter out OCR errors.
        """
        # Define realistic ranges (very broad to catch edge cases)
        realistic_ranges = {
            "Hemoglobin": (1.0, 25.0),
            "RBC": (1.0, 10.0),
            "WBC": (0.5, 100.0),
            "Platelets": (10.0, 1000.0),
            "MCV": (50.0, 150.0),
            "MCH": (15.0, 50.0),
            "MCHC": (25.0, 40.0),
            "Hematocrit": (15.0, 70.0),
        }
        
        if test_name in realistic_ranges:
            min_val, max_val = realistic_ranges[test_name]
            return min_val <= value <= max_val
        
        # If unknown test, allow it (better to include than exclude)
        return True
    
    @classmethod
    def clean_ocr_text(cls, text: str) -> str:
        """
        Clean OCR text by fixing common errors.
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned text
        """
        # Common OCR substitutions
        replacements = {
            'l': '1',  # lowercase L to 1 in numbers
            'O': '0',  # uppercase O to 0 in numbers
            'o': '0',  # lowercase o to 0 in numbers
            'S': '5',  # S to 5 in numbers
            'B': '8',  # B to 8 in numbers
            '|': '1',  # pipe to 1
        }
        
        # Fix numbers that have letter substitutions
        # Pattern: find numbers with letters mixed in
        def fix_number(match):
            num_str = match.group(0)
            for wrong, correct in replacements.items():
                num_str = num_str.replace(wrong, correct)
            return num_str
        
        # Apply to sequences that look like they should be numbers
        text = re.sub(r'\d+[lOoSB|]\d*\.?\d*', fix_number, text)
        
        return text
    
    @classmethod
    def parse_cbc_report(cls, text: str) -> Dict[str, any]:
        """
        Comprehensive CBC report parsing.
        
        Returns:
            Dictionary containing:
            - patient_info: Dict with demographics
            - test_values: Dict mapping test names to values
            - raw_text: Original text
        """
        # Clean OCR errors
        cleaned_text = cls.clean_ocr_text(text)
        
        # Extract patient information
        patient_info = cls.extract_patient_info(cleaned_text)
        
        # Extract test values
        test_values = cls.extract_test_values(cleaned_text)
        
        return {
            "patient_info": patient_info,
            "test_values": test_values,
            "raw_text": text
        }
