from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from enum import Enum


class SeverityLevel(str, Enum):
    NORMAL = "Normal"
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class AbnormalParameter:
    """Details of an abnormal test parameter"""
    test_name: str
    value: float
    expected_range: str
    status: str
    deviation: float
    clinical_significance: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_name": self.test_name,
            "value": self.value,
            "expected_range": self.expected_range,
            "status": self.status,
            "deviation_percentage": round(self.deviation, 2),
            "clinical_significance": self.clinical_significance
        }


@dataclass
class MedicalPattern:
    """Detected medical pattern"""
    condition: str
    confidence: float  # 0-100
    supporting_findings: List[str]
    suggested_specialty: str
    arabic_name: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "condition": self.condition,
            "confidence": round(self.confidence, 2),
            "supporting_findings": self.supporting_findings,
            "suggested_specialty": self.suggested_specialty,
            "arabic_name": self.arabic_name
        }


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    patient_summary: Dict[str, Any]
    test_results: Dict[str, Any]
    abnormal_parameters: List[AbnormalParameter]
    risk_score: int  # 0-100
    severity_level: SeverityLevel
    detected_patterns: List[MedicalPattern]
    suggested_specialty: Optional[str]
    arabic_explanation: str
    english_summary: str
    recommendations: List[str]
    visual_risk: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            "patient_summary": self.patient_summary,
            "test_results": self.test_results,
            "abnormal_parameters": [param.to_dict() for param in self.abnormal_parameters],
            "risk_score": self.risk_score,
            "severity_level": self.severity_level.value,
            "detected_patterns": [pattern.to_dict() for pattern in self.detected_patterns],
            "suggested_specialty": self.suggested_specialty,
            "arabic_explanation": self.arabic_explanation,
            "english_summary": self.english_summary,
            "recommendations": self.recommendations,
            "visual_risk": self.visual_risk

        }
    
    def to_json(self) -> Dict[str, Any]:
        """Alias for to_dict for backward compatibility"""
        return self.to_dict()
