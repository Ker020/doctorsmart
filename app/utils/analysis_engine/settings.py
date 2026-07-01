from typing import Dict, Tuple


class Settings:
    """Global configuration for the lab analysis system"""
    
    # Test type identifiers
    TEST_TYPE_CBC = "CBC"
    TEST_TYPE_LFT = "LFT"
    TEST_TYPE_KFT = "KFT"
    TEST_TYPE_LIPID = "Lipid Profile"
    
    # Risk scoring weights
    RISK_WEIGHTS = {
        "Hemoglobin": 1.5,      # High priority
        "WBC": 1.3,             # Infection marker
        "Platelets": 1.2,       # Bleeding risk
        "RBC": 1.0,
        "MCV": 0.8,
        "MCH": 0.7,
        "MCHC": 0.7,
        "Hematocrit": 0.9,
        "Neutrophils": 1.2,
        "Lymphocytes": 1.1
    }
    
    # Critical thresholds (percentage deviation that triggers critical status)
    CRITICAL_THRESHOLD_LOW = 30   # 30% below minimum
    CRITICAL_THRESHOLD_HIGH = 30  # 30% above maximum
    
    # Severity level thresholds
    SEVERITY_THRESHOLDS = {
        "LOW": (1, 25),
        "MODERATE": (26, 50),
        "HIGH": (51, 75),
        "CRITICAL": (76, 100)
    }
    
    # Pattern detection confidence thresholds
    PATTERN_CONFIDENCE_THRESHOLD = 60  # Minimum confidence to report pattern
    
    # Visualization
    RISK_BAR_LENGTH = 20
    RISK_BAR_FILLED = "█"
    RISK_BAR_EMPTY = "░"
    
    @staticmethod
    def get_severity_from_score(score: int) -> str:
        """Determine severity level from risk score"""
        if score == 0:
            return "Normal"
        elif score <= 25:
            return "Low"
        elif score <= 50:
            return "Moderate"
        elif score <= 75:
            return "High"
        else:
            return "Critical"


class CBCReferenceRanges:
    """CBC reference ranges with dynamic logic"""
    
    @staticmethod
    def get_hemoglobin_range(age: int, gender, pregnant: bool) -> Tuple[float, float]:
        """Get Hemoglobin reference range based on patient demographics"""
        if pregnant:
            return (11.0, 14.0)
        elif str(gender).lower() in ["female", "f"]:
            if age < 12:
                return (11.5, 15.5)
            else:
                return (12.0, 15.5)
        else:  # Male
            if age < 12:
                return (11.5, 15.5)
            else:
                return (13.5, 17.5)
    
    @staticmethod
    def get_rbc_range(age: int, gender, pregnant: bool) -> Tuple[float, float]:
        """Get RBC reference range"""
        if pregnant:
            return (3.8, 5.0)
        elif str(gender).lower() in ["female", "f"]:
            return (4.0, 5.2)
        else:
            return (4.5, 5.9)
    
    @staticmethod
    def get_wbc_range(age: int, gender, pregnant: bool) -> Tuple[float, float]:
        """Get WBC reference range"""
        if age < 2:
            return (6.0, 17.0)
        elif age < 12:
            return (4.5, 13.5)
        else:
            return (4.0, 11.0)
    
    @staticmethod
    def get_platelets_range(age: int, gender, pregnant: bool) -> Tuple[float, float]:
        """Get Platelets reference range"""
        return (150.0, 400.0)
    
    @staticmethod
    def get_mcv_range(age: int, gender, pregnant: bool) -> Tuple[float, float]:
        """Get MCV reference range"""
        if age < 2:
            return (70.0, 86.0)
        elif age < 12:
            return (77.0, 95.0)
        else:
            return (80.0, 100.0)
    
    @staticmethod
    def get_mch_range(age: int, gender, pregnant: bool) -> Tuple[float, float]:
        """Get MCH reference range"""
        return (27.0, 33.0)
    
    @staticmethod
    def get_mchc_range(age: int, gender, pregnant: bool) -> Tuple[float, float]:
        """Get MCHC reference range"""
        return (32.0, 36.0)
    
    @staticmethod
    def get_hematocrit_range(age: int, gender, pregnant: bool) -> Tuple[float, float]:
        """Get Hematocrit reference range"""
        if pregnant:
            return (33.0, 44.0)
        elif str(gender).lower() in ["female", "f"]:
            return (36.0, 46.0)
        else:
            return (40.0, 54.0)
    
    @staticmethod
    def get_range(test_name: str, age: int, gender, pregnant: bool) -> Tuple[float, float]:
        """Get reference range for any CBC test"""
        range_methods = {
            "Hemoglobin": CBCReferenceRanges.get_hemoglobin_range,
            "RBC": CBCReferenceRanges.get_rbc_range,
            "WBC": CBCReferenceRanges.get_wbc_range,
            "Platelets": CBCReferenceRanges.get_platelets_range,
            "MCV": CBCReferenceRanges.get_mcv_range,
            "MCH": CBCReferenceRanges.get_mch_range,
            "MCHC": CBCReferenceRanges.get_mchc_range,
            "Hematocrit": CBCReferenceRanges.get_hematocrit_range
        }
        
        method = range_methods.get(test_name)
        if method:
            return method(age, gender, pregnant)
        return None


# Create singleton instance
settings = Settings()
