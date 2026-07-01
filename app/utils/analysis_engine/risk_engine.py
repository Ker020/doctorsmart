from typing import Dict
from lab_test_models import TestResult, LabTest, TestStatus
from analysis_result_models import SeverityLevel
from settings import settings



class RiskEngine:
    """
    Intelligent risk scoring engine with weighted calculations.
    Considers test importance, deviation severity, and critical values.
    """
    
    @staticmethod
    def calculate_risk_score(lab_test: LabTest) -> tuple[int, SeverityLevel]:
        """
        Calculate comprehensive risk score based on all abnormalities.
        
        Args:
            lab_test: Complete lab test with results
            
        Returns:
            Tuple of (risk_score, severity_level)
        """
        results = lab_test.results
        
        if not results:
            return 0, SeverityLevel.NORMAL
        
        total_weighted_score = 0
        total_weight = 0
        
        for test_name, test_result in results.items():
            # Get weight for this test
            weight = settings.RISK_WEIGHTS.get(test_name, 1.0)
            
            # Calculate individual test risk
            test_risk = RiskEngine._calculate_test_risk(test_result)
            
            # Apply weight
            total_weighted_score += test_risk * weight
            total_weight += weight
        
        # Calculate average weighted score
        if total_weight > 0:
            risk_score = int((total_weighted_score / total_weight))
        else:
            risk_score = 0
        
        # Ensure within bounds
        risk_score = max(0, min(100, risk_score))
        
        # Determine severity level
        severity = RiskEngine._determine_severity(risk_score, lab_test)
        
        return risk_score, severity
    
    @staticmethod
    def _calculate_test_risk(test_result: TestResult) -> float:
        """
        Calculate risk score for individual test (0-100).
        
        Considers:
        - How far from normal range (deviation)
        - Whether it's critical or just abnormal
        - Direction (low vs high)
        """
        if test_result.status == TestStatus.NORMAL:
            return 0
        
        # Base risk on deviation percentage
        deviation = abs(test_result.deviation_percentage)
        
        # Calculate base risk from deviation
        base_risk = min(deviation, 100)
        
        # Apply multipliers based on status
        if test_result.status in [TestStatus.CRITICAL_LOW, TestStatus.CRITICAL_HIGH]:
            # Critical values are very serious
            risk = base_risk * 1.5
        elif test_result.status in [TestStatus.LOW, TestStatus.HIGH]:
            # Abnormal but not critical
            risk = base_risk * 1.0
        else:
            risk = 0
        
        # Apply additional weight for extreme deviations
        if deviation > 50:
            risk += 20
        elif deviation > 30:
            risk += 10
        
        return min(risk, 100)
    
    @staticmethod
    def _determine_severity(risk_score: int, lab_test: LabTest) -> SeverityLevel:
        """
        Determine severity level considering both risk score and critical tests.
        """
        # Check for any critical tests
        critical_tests = lab_test.get_critical_tests()
        
        # If any critical tests, minimum severity is HIGH
        if critical_tests:
            if risk_score >= 75:
                return SeverityLevel.CRITICAL
            else:
                return SeverityLevel.HIGH
        
        # Otherwise, use standard thresholds
        if risk_score == 0:
            return SeverityLevel.NORMAL
        elif risk_score <= 25:
            return SeverityLevel.LOW
        elif risk_score <= 50:
            return SeverityLevel.MODERATE
        elif risk_score <= 75:
            return SeverityLevel.HIGH
        else:
            return SeverityLevel.CRITICAL
    
    @staticmethod
    def generate_risk_summary(risk_score: int, severity: SeverityLevel, 
                            critical_tests: list[TestResult]) -> Dict[str, any]:
        """
        Generate a comprehensive risk summary.
        
        Returns:
            Dictionary with risk details
        """
        summary = {
            "risk_score": risk_score,
            "severity_level": severity.value,
            "critical_count": len(critical_tests),
            "requires_immediate_attention": severity in [SeverityLevel.HIGH, SeverityLevel.CRITICAL],
        }
        
        # Add interpretation
        if severity == SeverityLevel.NORMAL:
            summary["interpretation"] = "All tests within normal range"
            summary["interpretation_ar"] = "جميع التحاليل في المعدل الطبيعي"
        elif severity == SeverityLevel.LOW:
            summary["interpretation"] = "Minor abnormalities detected - routine follow-up recommended"
            summary["interpretation_ar"] = "تشوهات طفيفة - يُنصح بالمتابعة الروتينية"
        elif severity == SeverityLevel.MODERATE:
            summary["interpretation"] = "Moderate abnormalities - medical consultation recommended"
            summary["interpretation_ar"] = "تشوهات متوسطة - يُنصح باستشارة طبية"
        elif severity == SeverityLevel.HIGH:
            summary["interpretation"] = "Significant abnormalities - medical attention needed soon"
            summary["interpretation_ar"] = "تشوهات كبيرة - تحتاج لعناية طبية قريبًا"
        else:  # CRITICAL
            summary["interpretation"] = "Critical abnormalities - immediate medical attention required"
            summary["interpretation_ar"] = "تشوهات حرجة - تحتاج لعناية طبية فورية"
        
        return summary
    
    @staticmethod
    def calculate_individual_test_risks(results: Dict[str, TestResult]) -> Dict[str, float]:
        """
        Calculate risk score for each individual test.
        
        Returns:
            Dictionary mapping test names to risk scores
        """
        test_risks = {}
        
        for test_name, test_result in results.items():
            risk = RiskEngine._calculate_test_risk(test_result)
            test_risks[test_name] = round(risk, 2)
        
        return test_risks
