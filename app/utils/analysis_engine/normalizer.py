import re
from typing import Optional, Dict


class TestNameNormalizer:
    """
    Normalizes test names from various formats to standardized names.
    Handles OCR errors, abbreviations, and different naming conventions.
    """
    
    # Comprehensive alias mappings
    ALIASES = {
        # Hemoglobin variants
        "Hemoglobin": ["hemoglobin", "hb", "hgb", "hæmoglobin", "haemoglobin", 
                       "hemoglob", "hemog", "hemo", "hgb level"],
        
        # WBC variants
        "WBC": ["wbc", "wbcs", "white blood cells", "white blood cell", "wbc count",
                "white cell", "white cells", "leucocytes", "leukocytes", "wcc",
                "total wbc", "twbc"],
        
        # RBC variants
        "RBC": ["rbc", "rbcs", "red blood cells", "red blood cell", "rbc count",
                "red cell", "red cells", "erythrocytes", "rcc", "total rbc", "trbc"],
        
        # Platelets variants
        "Platelets": ["platelets", "platelet", "plt", "plts", "platelet count",
                      "thrombocytes", "plt count"],
        
        # MCV variants
        "MCV": ["mcv", "mean corpuscular volume", "mean cell volume"],
        
        # MCH variants
        "MCH": ["mch", "mean corpuscular hemoglobin", "mean cell hemoglobin",
                "mean corpuscular hgb"],
        
        # MCHC variants
        "MCHC": ["mchc", "mean corpuscular hemoglobin concentration",
                 "mean cell hemoglobin concentration", "mean corpuscular hgb conc"],
        
        # Hematocrit variants
        "Hematocrit": ["hematocrit", "hct", "hct%", "haematocrit", "hct percentage",
                       "packed cell volume", "pcv"],
        
        # Differential counts
        "Neutrophils": ["neutrophils", "neutrophil", "neut", "neutro", "pmn",
                        "polymorphonuclear", "segmented neutrophils", "segs"],
        
        "Lymphocytes": ["lymphocytes", "lymphocyte", "lymph", "lymphs"],
        
        "Monocytes": ["monocytes", "monocyte", "mono", "monos"],
        
        "Eosinophils": ["eosinophils", "eosinophil", "eos", "eosino"],
        
        "Basophils": ["basophils", "basophil", "baso", "basos"],
        
        # ESR
        "ESR": ["esr", "erythrocyte sedimentation rate", "sed rate", "sedimentation rate"]
    }
    
    # Build reverse lookup for faster search
    _REVERSE_MAP: Dict[str, str] = {}
    
    @classmethod
    def _build_reverse_map(cls):
        """Build reverse mapping from all aliases to standard names"""
        if not cls._REVERSE_MAP:
            for standard_name, aliases in cls.ALIASES.items():
                for alias in aliases:
                    cls._REVERSE_MAP[alias.lower()] = standard_name
    
    @classmethod
    def normalize(cls, test_name: str) -> Optional[str]:
        """
        Normalize a test name to its standard form.
        
        Args:
            test_name: Raw test name from lab report
            
        Returns:
            Standardized test name or None if not recognized
        """
        if not test_name:
            return None
        
        # Build reverse map on first use
        cls._build_reverse_map()
        
        # Clean the input
        cleaned = cls._clean_name(test_name)
        
        if not cleaned:
            return None
        
        # Direct lookup
        standard = cls._REVERSE_MAP.get(cleaned.lower())
        if standard:
            return standard
        
        # Try fuzzy matching for OCR errors
        standard = cls._fuzzy_match(cleaned)
        if standard:
            return standard
        
        return None
    
    @staticmethod
    def _clean_name(name: str) -> str:
        """Clean test name by removing special characters and extra whitespace"""
        # Remove units in parentheses
        name = re.sub(r'\([^)]*\)', '', name)
        
        # Remove common separators and special chars
        name = re.sub(r'[:\-\=\>\<\*\#]', ' ', name)
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        return name.strip()
    
    @classmethod
    def _fuzzy_match(cls, name: str) -> Optional[str]:
        """
        Attempt fuzzy matching for OCR errors.
        Uses simple character substitution for common OCR mistakes.
        """
        # Common OCR substitutions
        ocr_fixes = {
            '0': 'o',
            '1': 'i',
            '5': 's',
            '8': 'b',
        }
        
        name_lower = name.lower()
        
        # Try with OCR fixes
        for wrong, correct in ocr_fixes.items():
            if wrong in name_lower:
                fixed = name_lower.replace(wrong, correct)
                if fixed in cls._REVERSE_MAP:
                    return cls._REVERSE_MAP[fixed]
        
        # Try partial matching for longer names
        for alias, standard in cls._REVERSE_MAP.items():
            if len(name_lower) > 4:  # Only for reasonably long names
                # Check if name contains the alias or vice versa
                if alias in name_lower or name_lower in alias:
                    # Additional check: similarity should be high
                    if cls._similarity_check(name_lower, alias):
                        return standard
        
        return None
    
    @staticmethod
    def _similarity_check(str1: str, str2: str) -> bool:
        """Check if two strings are similar enough"""
        # Simple check: common prefix length
        min_len = min(len(str1), len(str2))
        common_prefix = sum(1 for i in range(min_len) if str1[i] == str2[i])
        
        # Require at least 70% similarity
        return (common_prefix / max(len(str1), len(str2))) >= 0.7
    
    @classmethod
    def get_all_standard_names(cls) -> list[str]:
        """Get list of all standard test names"""
        return list(cls.ALIASES.keys())


# Create module-level function for convenience
def normalize_test_name(test_name: str) -> Optional[str]:
    """Convenience function to normalize test names"""
    return TestNameNormalizer.normalize(test_name)
