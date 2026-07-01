from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class TestStatus(str, Enum):
    NORMAL = "Normal"
    LOW = "Low"
    HIGH = "High"
    CRITICAL_LOW = "Critical Low"
    CRITICAL_HIGH = "Critical High"


@dataclass
class PatientInfo:
    """Patient demographic information"""
    age: int
    gender: Gender
    pregnant: bool = False
    patient_name: Optional[str] = None
    patient_id: Optional[str] = None
    test_date: Optional[str] = None
    lab_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "patient_name": self.patient_name,
            "patient_id": self.patient_id,
            "age": self.age,
            "gender": self.gender.value,
            "pregnant": self.pregnant,
            "test_date": self.test_date,
            "lab_name": self.lab_name
        }


@dataclass
class TestResult:
    """Individual test result"""
    test_name: str
    value: float
    unit: Optional[str]
    reference_range: tuple[float, float]
    status: TestStatus
    deviation_percentage: float  # How far from normal range
    
    def is_abnormal(self) -> bool:
        return self.status not in [TestStatus.NORMAL]
    
    def is_critical(self) -> bool:
        return self.status in [TestStatus.CRITICAL_LOW, TestStatus.CRITICAL_HIGH]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_name": self.test_name,
            "value": self.value,
            "unit": self.unit,
            "reference_range": {
                "min": self.reference_range[0],
                "max": self.reference_range[1]
            },
            "status": self.status.value,
            "deviation_percentage": round(self.deviation_percentage, 2)
        }


@dataclass
class LabTest:
    """Container for all lab test information"""
    test_type: str  # "CBC", "LFT", "KFT", etc.
    patient_info: PatientInfo
    results: Dict[str, TestResult]
    raw_text: Optional[str] = None
    
    def get_abnormal_tests(self) -> list[TestResult]:
        return [test for test in self.results.values() if test.is_abnormal()]
    
    def get_critical_tests(self) -> list[TestResult]:
        return [test for test in self.results.values() if test.is_critical()]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_type": self.test_type,
            "patient_info": self.patient_info.to_dict(),
            "results": {name: result.to_dict() for name, result in self.results.items()}
        }
