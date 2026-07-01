from typing import List, Dict, Optional
from lab_test_models import TestResult, LabTest, TestStatus
from analysis_result_models import MedicalPattern



class PatternDetector:
    """
    Detects medical patterns and conditions from CBC results.
    Uses rule-based logic combined with confidence scoring.
    """
    
    @staticmethod
    def detect_patterns(lab_test: LabTest) -> List[MedicalPattern]:
        """
        Detect all possible medical patterns from lab results.
        
        Args:
            lab_test: Complete lab test with results
            
        Returns:
            List of detected patterns with confidence scores
        """
        patterns = []
        results = lab_test.results
        
        # Check each pattern
        patterns.extend(PatternDetector._detect_iron_deficiency_anemia(results))
        patterns.extend(PatternDetector._detect_infection_pattern(results))
        patterns.extend(PatternDetector._detect_vitamin_b12_deficiency(results))
        patterns.extend(PatternDetector._detect_thalassemia_trait(results))
        patterns.extend(PatternDetector._detect_bleeding_risk(results))
        patterns.extend(PatternDetector._detect_dehydration(results))
        patterns.extend(PatternDetector._detect_chronic_inflammation(results))
        patterns.extend(PatternDetector._detect_bone_marrow_issues(results))
        
        # Sort by confidence
        patterns.sort(key=lambda p: p.confidence, reverse=True)
        
        # Filter by minimum confidence threshold
        patterns = [p for p in patterns if p.confidence >= 60]
        
        return patterns
    
    @staticmethod
    def _detect_iron_deficiency_anemia(results: Dict[str, TestResult]) -> List[MedicalPattern]:
        """
        Detect iron deficiency anemia pattern.
        Classic signs: Low Hb, Low RBC, Low MCV (microcytic)
        """
        patterns = []
        
        hb = results.get("Hemoglobin")
        rbc = results.get("RBC")
        mcv = results.get("MCV")
        
        if not all([hb, rbc, mcv]):
            return patterns
        
        # Calculate confidence based on findings
        confidence = 0
        findings = []
        
        # Low hemoglobin (major criterion)
        if hb.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            confidence += 40
            findings.append(f"Low Hemoglobin ({hb.value} g/dL)")
        
        # Low RBC (supporting criterion)
        if rbc.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            confidence += 20
            findings.append(f"Low RBC count ({rbc.value} x10^6/µL)")
        
        # Low MCV - microcytic (key criterion)
        if mcv.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            confidence += 30
            findings.append(f"Microcytic cells - Low MCV ({mcv.value} fL)")
        
        # Check MCH if available
        mch = results.get("MCH")
        if mch and mch.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            confidence += 10
            findings.append(f"Low MCH ({mch.value} pg)")
        
        if confidence >= 60:
            pattern = MedicalPattern(
                condition="Iron Deficiency Anemia",
                confidence=min(confidence, 95),  # Cap at 95%
                supporting_findings=findings,
                suggested_specialty="Hematology / أمراض الدم",
                arabic_name="أنيميا نقص الحديد"
            )
            patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def _detect_infection_pattern(results: Dict[str, TestResult]) -> List[MedicalPattern]:
        """
        Detect acute infection pattern.
        Classic sign: Elevated WBC
        """
        patterns = []
        
        wbc = results.get("WBC")
        
        if not wbc:
            return patterns
        
        confidence = 0
        findings = []
        
        # High WBC (primary indicator)
        if wbc.status == TestStatus.HIGH:
            confidence = 70
            findings.append(f"Elevated WBC ({wbc.value} x10^3/µL)")
        elif wbc.status == TestStatus.CRITICAL_HIGH:
            confidence = 85
            findings.append(f"Significantly elevated WBC ({wbc.value} x10^3/µL)")
        
        # Very high WBC suggests acute infection
        if wbc.value > 15.0:
            confidence += 10
        
        if confidence >= 60:
            pattern = MedicalPattern(
                condition="Possible Acute Infection or Inflammation",
                confidence=min(confidence, 90),
                supporting_findings=findings,
                suggested_specialty="Internal Medicine / الباطنة",
                arabic_name="احتمال وجود عدوى أو التهاب حاد"
            )
            patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def _detect_vitamin_b12_deficiency(results: Dict[str, TestResult]) -> List[MedicalPattern]:
        """
        Detect Vitamin B12 or Folate deficiency.
        Classic signs: Low Hb, Low RBC, High MCV (macrocytic)
        """
        patterns = []
        
        hb = results.get("Hemoglobin")
        rbc = results.get("RBC")
        mcv = results.get("MCV")
        
        if not all([hb, mcv]):
            return patterns
        
        confidence = 0
        findings = []
        
        # Low hemoglobin
        if hb and hb.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            confidence += 30
            findings.append(f"Low Hemoglobin ({hb.value} g/dL)")
        
        # High MCV - macrocytic (key criterion)
        if mcv.status in [TestStatus.HIGH, TestStatus.CRITICAL_HIGH]:
            confidence += 50
            findings.append(f"Macrocytic cells - High MCV ({mcv.value} fL)")
        
        # Low RBC
        if rbc and rbc.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            confidence += 20
            findings.append(f"Low RBC count ({rbc.value} x10^6/µL)")
        
        if confidence >= 60:
            pattern = MedicalPattern(
                condition="Possible Vitamin B12 or Folate Deficiency",
                confidence=min(confidence, 85),
                supporting_findings=findings,
                suggested_specialty="Hematology / أمراض الدم",
                arabic_name="احتمال نقص فيتامين ب12 أو حمض الفوليك"
            )
            patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def _detect_thalassemia_trait(results: Dict[str, TestResult]) -> List[MedicalPattern]:
        """
        Detect Thalassemia trait.
        Classic signs: Low/Normal Hb, High RBC, Low MCV
        """
        patterns = []
        
        hb = results.get("Hemoglobin")
        rbc = results.get("RBC")
        mcv = results.get("MCV")
        
        if not all([hb, rbc, mcv]):
            return patterns
        
        confidence = 0
        findings = []
        
        # Normal or slightly low Hb
        if hb.status in [TestStatus.NORMAL, TestStatus.LOW]:
            confidence += 20
            findings.append(f"Hemoglobin {hb.value} g/dL")
        
        # High RBC (key criterion)
        if rbc.status in [TestStatus.HIGH, TestStatus.CRITICAL_HIGH]:
            confidence += 40
            findings.append(f"Elevated RBC count ({rbc.value} x10^6/µL)")
        
        # Low MCV (key criterion)
        if mcv.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            confidence += 35
            findings.append(f"Microcytic cells - Low MCV ({mcv.value} fL)")
        
        # RBC/MCV ratio check (specific for thalassemia)
        if rbc.value > 5.0 and mcv.value < 80:
            confidence += 10
        
        if confidence >= 65:
            pattern = MedicalPattern(
                condition="Possible Thalassemia Trait",
                confidence=min(confidence, 80),
                supporting_findings=findings,
                suggested_specialty="Hematology / أمراض الدم",
                arabic_name="احتمال وجود ثلاسيميا (أنيميا البحر المتوسط)"
            )
            patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def _detect_bleeding_risk(results: Dict[str, TestResult]) -> List[MedicalPattern]:
        """
        Detect bleeding risk from low platelets.
        """
        patterns = []
        
        platelets = results.get("Platelets")
        
        if not platelets:
            return patterns
        
        confidence = 0
        findings = []
        
        if platelets.status == TestStatus.LOW:
            confidence = 65
            findings.append(f"Low platelet count ({platelets.value} x10^3/µL)")
        elif platelets.status == TestStatus.CRITICAL_LOW:
            confidence = 90
            findings.append(f"Critically low platelet count ({platelets.value} x10^3/µL)")
        
        if confidence >= 60:
            pattern = MedicalPattern(
                condition="Thrombocytopenia - Bleeding Risk",
                confidence=confidence,
                supporting_findings=findings,
                suggested_specialty="Hematology / أمراض الدم",
                arabic_name="نقص الصفائح الدموية - خطر النزيف"
            )
            patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def _detect_dehydration(results: Dict[str, TestResult]) -> List[MedicalPattern]:
        """
        Detect possible dehydration.
        Signs: High Hb, High Hematocrit, High RBC
        """
        patterns = []
        
        hb = results.get("Hemoglobin")
        rbc = results.get("RBC")
        hct = results.get("Hematocrit")
        
        if not hb:
            return patterns
        
        confidence = 0
        findings = []
        
        # High hemoglobin
        if hb.status in [TestStatus.HIGH, TestStatus.CRITICAL_HIGH]:
            confidence += 30
            findings.append(f"Elevated Hemoglobin ({hb.value} g/dL)")
        
        # High RBC
        if rbc and rbc.status in [TestStatus.HIGH, TestStatus.CRITICAL_HIGH]:
            confidence += 25
            findings.append(f"Elevated RBC ({rbc.value} x10^6/µL)")
        
        # High Hematocrit
        if hct and hct.status in [TestStatus.HIGH, TestStatus.CRITICAL_HIGH]:
            confidence += 30
            findings.append(f"Elevated Hematocrit ({hct.value}%)")
        
        if confidence >= 60:
            pattern = MedicalPattern(
                condition="Possible Dehydration or Polycythemia",
                confidence=min(confidence, 75),
                supporting_findings=findings,
                suggested_specialty="Internal Medicine / الباطنة",
                arabic_name="احتمال جفاف أو زيادة كريات الدم الحمراء"
            )
            patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def _detect_chronic_inflammation(results: Dict[str, TestResult]) -> List[MedicalPattern]:
        """
        Detect chronic inflammation pattern.
        Signs: Mild anemia with normal MCV, slightly elevated WBC
        """
        patterns = []
        
        hb = results.get("Hemoglobin")
        wbc = results.get("WBC")
        mcv = results.get("MCV")
        
        if not all([hb, wbc]):
            return patterns
        
        confidence = 0
        findings = []
        
        # Mild anemia
        if hb.status == TestStatus.LOW and hb.value > 10.0:
            confidence += 25
            findings.append(f"Mild anemia - Hb {hb.value} g/dL")
        
        # Normal MCV (normocytic)
        if mcv and mcv.status == TestStatus.NORMAL:
            confidence += 20
            findings.append(f"Normocytic cells - MCV {mcv.value} fL")
        
        # Mildly elevated WBC
        if wbc.status == TestStatus.HIGH and wbc.value < 15.0:
            confidence += 25
            findings.append(f"Mildly elevated WBC ({wbc.value} x10^3/µL)")
        
        if confidence >= 60:
            pattern = MedicalPattern(
                condition="Possible Chronic Inflammation",
                confidence=min(confidence, 70),
                supporting_findings=findings,
                suggested_specialty="Internal Medicine / الباطنة",
                arabic_name="احتمال التهاب مزمن"
            )
            patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def _detect_bone_marrow_issues(results: Dict[str, TestResult]) -> List[MedicalPattern]:
        """
        Detect possible bone marrow suppression.
        Signs: Pancytopenia (low RBC, WBC, and Platelets)
        """
        patterns = []
        
        hb = results.get("Hemoglobin")
        wbc = results.get("WBC")
        platelets = results.get("Platelets")
        
        if not all([hb, wbc, platelets]):
            return patterns
        
        confidence = 0
        findings = []
        
        low_count = 0
        
        if hb.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            low_count += 1
            findings.append(f"Low Hemoglobin ({hb.value} g/dL)")
        
        if wbc.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            low_count += 1
            findings.append(f"Low WBC ({wbc.value} x10^3/µL)")
        
        if platelets.status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            low_count += 1
            findings.append(f"Low Platelets ({platelets.value} x10^3/µL)")
        
        # Pancytopenia: at least 2 cell lines affected
        if low_count >= 2:
            confidence = 50 + (low_count * 15)
            
            pattern = MedicalPattern(
                condition="Possible Bone Marrow Suppression (Pancytopenia)",
                confidence=min(confidence, 85),
                supporting_findings=findings,
                suggested_specialty="Hematology - Urgent / أمراض الدم - عاجل",
                arabic_name="احتمال كبت نخاع العظم"
            )
            patterns.append(pattern)
        
        return patterns
