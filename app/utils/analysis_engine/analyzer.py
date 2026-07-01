from typing import Dict, Optional

from lab_test_models import LabTest, TestResult, PatientInfo, Gender, TestStatus
from analysis_result_models import AnalysisResult, AbnormalParameter, SeverityLevel
from settings import CBCReferenceRanges, settings
from parser import LabReportParser
from pattern_detector import PatternDetector
from risk_engine import RiskEngine
from explanation_generator import ExplanationGenerator
from visualizer import RiskVisualizer



class CBCAnalyzer:
    """
    Main analyzer that orchestrates the complete CBC analysis workflow.
    """
    
    def __init__(self):
        self.parser = LabReportParser()
        self.pattern_detector = PatternDetector()
        self.risk_engine = RiskEngine()
        self.explanation_generator = ExplanationGenerator()
        self.visualizer = RiskVisualizer()
    
    def analyze(
        self,
        text: str,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        pregnant: bool = False
    ) -> AnalysisResult:
        """
        Perform complete CBC analysis.
        
        Args:
            text: Raw text from lab report
            age: Patient age (extracted from report if not provided)
            gender: Patient gender (extracted from report if not provided)
            pregnant: Pregnancy status
            
        Returns:
            Complete AnalysisResult object
        """
        # Step 1: Parse the report
        parsed_data = self.parser.parse_cbc_report(text)
        
        # Step 2: Build patient info
        patient_info = self._build_patient_info(
            parsed_data["patient_info"],
            age,
            gender,
            pregnant
        )
        
        # Step 3: Process test results
        test_results = self._process_test_results(
            parsed_data["test_values"],
            patient_info
        )
        
        # Step 4: Build LabTest object
        lab_test = LabTest(
            test_type="CBC",
            patient_info=patient_info,
            results=test_results,
            raw_text=text
        )
        
        # Step 5: Detect patterns
        detected_patterns = self.pattern_detector.detect_patterns(lab_test)
        
        # Step 6: Calculate risk
        risk_score, severity_level = self.risk_engine.calculate_risk_score(lab_test)
        
        # Step 7: Generate abnormal parameters list
        abnormal_params = self._build_abnormal_parameters(lab_test)
        
        # Step 8: Determine suggested specialty
        suggested_specialty = self._determine_specialty(detected_patterns)
        
        # Step 9: Generate explanations
        arabic_explanation = self.explanation_generator.generate_arabic_explanation(
            lab_test,
            abnormal_params,
            detected_patterns,
            risk_score,
            severity_level
        )
        
        english_summary = self.explanation_generator.generate_english_summary(
            lab_test,
            abnormal_params,
            detected_patterns,
            risk_score,
            severity_level
        )
        
        # Step 10: Generate visual risk display
        visual_risk = self.visualizer.generate_colored_risk_bar(risk_score)
        
        # Step 11: Generate recommendations
        recommendations = self._generate_recommendations(
            severity_level,
            detected_patterns,
            abnormal_params
        )
        
        # Step 12: Build final result
        result = AnalysisResult(
            patient_summary=patient_info.to_dict(),
            test_results=lab_test.to_dict()["results"],
            abnormal_parameters=abnormal_params,
            risk_score=risk_score,
            severity_level=severity_level,
            detected_patterns=detected_patterns,
            suggested_specialty=suggested_specialty,
            arabic_explanation=arabic_explanation,
            english_summary=english_summary,
            recommendations=recommendations,
            visual_risk=visual_risk
        )
        
        return result
    
    def _build_patient_info(
        self,
        parsed_info: Dict,
        age: Optional[int],
        gender: Optional[str],
        pregnant: bool
    ) -> PatientInfo:
        """Build PatientInfo from parsed data and provided parameters"""
        
        # Use provided age/gender or fall back to parsed
        final_age = age if age is not None else (
            int(parsed_info["age"]) if parsed_info.get("age") else 30
        )
        
        final_gender = gender if gender is not None else (
            parsed_info.get("gender", "male")
        )
        
        # Convert gender string to enum
        gender_enum = Gender.MALE if final_gender.lower() in ["male", "m"] else Gender.FEMALE
        
        return PatientInfo(
            age=final_age,
            gender=gender_enum,
            pregnant=pregnant,
            patient_name=parsed_info.get("patient_name"),
            patient_id=parsed_info.get("patient_id"),
            test_date=parsed_info.get("date"),
            lab_name=parsed_info.get("lab_name")
        )
    
    def _process_test_results(
        self,
        test_values: Dict[str, float],
        patient_info: PatientInfo
    ) -> Dict[str, TestResult]:
        """
        Process raw test values into TestResult objects.
        """
        results = {}
        
        for test_name, value in test_values.items():
            # Get reference range
            ref_range = CBCReferenceRanges.get_range(
                test_name,
                patient_info.age,
                patient_info.gender,
                patient_info.pregnant
            )
            
            if not ref_range:
                continue
            
            min_val, max_val = ref_range
            
            # Determine status
            status, deviation = self._determine_status(value, min_val, max_val)
            
            # Create TestResult
            test_result = TestResult(
                test_name=test_name,
                value=value,
                unit=self._get_unit(test_name),
                reference_range=ref_range,
                status=status,
                deviation_percentage=deviation
            )
            
            results[test_name] = test_result
        
        return results
    
    def _determine_status(
        self,
        value: float,
        min_val: float,
        max_val: float
    ) -> tuple[TestStatus, float]:
        """
        Determine test status and calculate deviation percentage.
        """
        if value < min_val:
            # Calculate how far below minimum
            deviation = ((min_val - value) / min_val) * 100
            
            if deviation >= settings.CRITICAL_THRESHOLD_LOW:
                status = TestStatus.CRITICAL_LOW
            else:
                status = TestStatus.LOW
                
        elif value > max_val:
            # Calculate how far above maximum
            deviation = ((value - max_val) / max_val) * 100
            
            if deviation >= settings.CRITICAL_THRESHOLD_HIGH:
                status = TestStatus.CRITICAL_HIGH
            else:
                status = TestStatus.HIGH
        else:
            status = TestStatus.NORMAL
            deviation = 0
        
        return status, deviation
    
    def _get_unit(self, test_name: str) -> Optional[str]:
        """Get appropriate unit for test"""
        units = {
            "Hemoglobin": "g/dL",
            "RBC": "x10^6/µL",
            "WBC": "x10^3/µL",
            "Platelets": "x10^3/µL",
            "MCV": "fL",
            "MCH": "pg",
            "MCHC": "g/dL",
            "Hematocrit": "%"
        }
        return units.get(test_name)
    
    def _build_abnormal_parameters(self, lab_test: LabTest) -> list[AbnormalParameter]:
        """Build list of abnormal parameters with details"""
        abnormal_params = []
        
        for test_result in lab_test.get_abnormal_tests():
            min_val, max_val = test_result.reference_range
            expected_range = f"{min_val} - {max_val}"
            
            clinical_sig = self.explanation_generator.generate_clinical_significance(
                test_result.test_name,
                test_result.status
            )
            
            param = AbnormalParameter(
                test_name=test_result.test_name,
                value=test_result.value,
                expected_range=expected_range,
                status=test_result.status.value,
                deviation=test_result.deviation_percentage,
                clinical_significance=clinical_sig
            )
            
            abnormal_params.append(param)
        
        # Sort by deviation (most severe first)
        abnormal_params.sort(key=lambda p: p.deviation, reverse=True)
        
        return abnormal_params
    
    def _determine_specialty(self, patterns: list) -> Optional[str]:
        """Determine the most appropriate medical specialty"""
        if not patterns:
            return None
        
        # Return the specialty from the highest confidence pattern
        return patterns[0].suggested_specialty
    
    def _generate_recommendations(
        self,
        severity: SeverityLevel,
        patterns: list,
        abnormal_params: list
    ) -> list[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if severity == SeverityLevel.NORMAL:
            recommendations.append("Continue regular health checkups")
            recommendations.append("Maintain a balanced diet and healthy lifestyle")
        
        elif severity == SeverityLevel.LOW:
            recommendations.append("Schedule a routine follow-up with your doctor")
            recommendations.append("Monitor your symptoms")
            if patterns:
                recommendations.append(f"Discuss {patterns[0].condition.lower()} with your physician")
        
        elif severity == SeverityLevel.MODERATE:
            recommendations.append("Consult with a physician within 1-2 weeks")
            recommendations.append("Bring this report to your appointment")
            if patterns:
                recommendations.append(f"Further evaluation for {patterns[0].condition.lower()} recommended")
        
        elif severity == SeverityLevel.HIGH:
            recommendations.append("Seek medical attention within 2-3 days")
            recommendations.append("Do not delay consultation")
            if any("Critical" in p.status for p in abnormal_params):
                recommendations.append("Some values are critical - prioritize medical evaluation")
        
        else:  # CRITICAL
            recommendations.append("⚠️ Seek immediate medical attention")
            recommendations.append("Contact your healthcare provider today")
            recommendations.append("Consider emergency department if symptomatic")
            if patterns:
                recommendations.append(f"Critical findings suggest {patterns[0].condition.lower()}")
        
        return recommendations


# Convenience function
def analyze_cbc(
    text: str,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    pregnant: bool = False
) -> AnalysisResult:
    """
    Convenience function to analyze CBC report.
    
    Args:
        text: Lab report text
        age: Patient age
        gender: Patient gender ("male" or "female")
        pregnant: Pregnancy status
        
    Returns:
        Complete analysis result
    """
    analyzer = CBCAnalyzer()
    return analyzer.analyze(text, age, gender, pregnant)
