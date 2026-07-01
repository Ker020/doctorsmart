from typing import List
from lab_test_models import TestResult, LabTest, TestStatus
from analysis_result_models import MedicalPattern, SeverityLevel, AbnormalParameter



class ExplanationGenerator:
    """
    Generates bilingual (Arabic & English) medical explanations.
    Arabic tone: Simple, Egyptian-friendly
    English tone: Professional medical summary
    """
    
    @staticmethod
    def generate_arabic_explanation(
        lab_test: LabTest,
        abnormal_params: List[AbnormalParameter],
        patterns: List[MedicalPattern],
        risk_score: int,
        severity: SeverityLevel
    ) -> str:
        """
        Generate Egyptian Arabic explanation with friendly tone.
        """
        explanation = "📊 **شرح نتيجة التحليل**\n\n"
        
        # Summary of results
        total_tests = len(lab_test.results)
        abnormal_count = len(abnormal_params)
        normal_count = total_tests - abnormal_count
        
        if abnormal_count == 0:
            explanation += "✅ **الحمد لله، كل التحاليل طبيعية!**\n\n"
            explanation += f"📋 تم فحص {total_tests} تحليل وكلهم في المعدل الطبيعي.\n"
            return explanation
        
        explanation += f"📋 **ملخص النتائج:**\n"
        explanation += f"• إجمالي التحاليل: {total_tests}\n"
        explanation += f"• طبيعي: {normal_count} ✅\n"
        explanation += f"• غير طبيعي: {abnormal_count} ⚠️\n\n"
        
        # Detail abnormal tests
        explanation += "🔍 **التحاليل اللي محتاجة انتباه:**\n\n"
        
        for param in abnormal_params:
            explanation += f"• **{param.test_name}**: {param.value}\n"
            
            if "Low" in param.status:
                explanation += f"  📉 أقل من الطبيعي (المفروض: {param.expected_range})\n"
            else:
                explanation += f"  📈 أعلى من الطبيعي (المفروض: {param.expected_range})\n"
            
            # Add simple explanation
            if param.clinical_significance:
                explanation += f"  💡 {param.clinical_significance}\n"
            
            explanation += "\n"
        
        # Add detected patterns
        if patterns:
            explanation += "🧠 **التقييم الطبي المبدئي:**\n\n"
            
            for pattern in patterns:
                explanation += f"• **{pattern.arabic_name}**\n"
                explanation += f"  📊 احتمالية: {pattern.confidence:.0f}%\n"
                
                if pattern.supporting_findings:
                    explanation += "  🔬 بناءً على:\n"
                    for finding in pattern.supporting_findings[:3]:  # Top 3 findings
                        explanation += f"    - {finding}\n"
                
                explanation += "\n"
        
        # Risk assessment
        explanation += f"⚠️ **تقييم الخطورة:** {risk_score}%\n"
        explanation += f"📊 **مستوى الخطورة:** {ExplanationGenerator._get_severity_arabic(severity)}\n\n"
        
        # Recommendations
        explanation += "💊 **التوصيات:**\n\n"
        
        if severity == SeverityLevel.NORMAL:
            explanation += "✅ كل شيء تمام! استمر في نمط حياة صحي.\n"
        elif severity == SeverityLevel.LOW:
            explanation += "• راجع دكتور عادي للمتابعة\n"
            explanation += "• مفيش داعي للقلق، بس متابعة روتينية\n"
        elif severity == SeverityLevel.MODERATE:
            explanation += "• يُفضل تراجع دكتور في أقرب وقت\n"
            explanation += "• ممكن تحتاج تحاليل إضافية\n"
        elif severity == SeverityLevel.HIGH:
            explanation += "⚠️ يُفضل تراجع دكتور بسرعة\n"
            explanation += "• النتائج محتاجة تقييم طبي\n"
        else:  # CRITICAL
            explanation += "🚨 **مهم جداً: راجع دكتور فوراً!**\n"
            explanation += "• النتائج فيها قيم حرجة\n"
            explanation += "• متأخرش في المتابعة الطبية\n"
        
        # Add suggested specialty if patterns detected
        if patterns and patterns[0].suggested_specialty:
            specialty_ar = patterns[0].suggested_specialty.split("/")[-1].strip()
            explanation += f"\n👨‍⚕️ **التخصص المقترح:** {specialty_ar}\n"
        
        # Disclaimer
        explanation += "\n" + "─" * 50 + "\n"
        explanation += "⚠️ **ملحوظة مهمة:**\n"
        explanation += "ده تقييم أولي بيساعدك تفهم النتيجة، لكن **مش بديل عن استشارة الدكتور**.\n"
        explanation += "الدكتور هو اللي يقدر يشخص ويعمل خطة علاج مناسبة ليك.\n"
        
        return explanation
    
    @staticmethod
    def generate_english_summary(
        lab_test: LabTest,
        abnormal_params: List[AbnormalParameter],
        patterns: List[MedicalPattern],
        risk_score: int,
        severity: SeverityLevel
    ) -> str:
        """
        Generate professional English medical summary.
        """
        summary = "📋 **COMPLETE BLOOD COUNT (CBC) ANALYSIS REPORT**\n\n"
        
        # Patient info
        if lab_test.patient_info:
            pi = lab_test.patient_info
            summary += "**Patient Information:**\n"
            if pi.patient_name:
                summary += f"Name: {pi.patient_name}\n"
            summary += f"Age: {pi.age} years | Gender: {pi.gender.value.capitalize()}\n"
            if pi.test_date:
                summary += f"Test Date: {pi.test_date}\n"
            summary += "\n"
        
        # Results summary
        total_tests = len(lab_test.results)
        abnormal_count = len(abnormal_params)
        
        summary += "**RESULTS SUMMARY:**\n"
        summary += f"Total Parameters Tested: {total_tests}\n"
        summary += f"Within Normal Range: {total_tests - abnormal_count}\n"
        summary += f"Abnormal Values: {abnormal_count}\n\n"
        
        if abnormal_count == 0:
            summary += "✅ **All parameters within normal reference ranges.**\n"
            summary += "No significant abnormalities detected.\n"
            return summary
        
        # Abnormal findings
        summary += "**ABNORMAL FINDINGS:**\n\n"
        
        # Group by severity
        critical = [p for p in abnormal_params if "Critical" in p.status]
        high = [p for p in abnormal_params if p.status == "High" and "Critical" not in p.status]
        low = [p for p in abnormal_params if p.status == "Low" and "Critical" not in p.status]
        
        if critical:
            summary += "🔴 **Critical Values:**\n"
            for param in critical:
                summary += f"• {param.test_name}: {param.value} (Expected: {param.expected_range})\n"
                summary += f"  Status: {param.status} - Deviation: {param.deviation:.1f}%\n"
            summary += "\n"
        
        if high:
            summary += "📈 **Elevated Values:**\n"
            for param in high:
                summary += f"• {param.test_name}: {param.value} (Expected: {param.expected_range})\n"
            summary += "\n"
        
        if low:
            summary += "📉 **Decreased Values:**\n"
            for param in low:
                summary += f"• {param.test_name}: {param.value} (Expected: {param.expected_range})\n"
            summary += "\n"
        
        # Clinical interpretation
        if patterns:
            summary += "**CLINICAL INTERPRETATION:**\n\n"
            
            for i, pattern in enumerate(patterns, 1):
                summary += f"{i}. **{pattern.condition}** (Confidence: {pattern.confidence:.0f}%)\n"
                summary += f"   Supporting Findings:\n"
                for finding in pattern.supporting_findings:
                    summary += f"   • {finding}\n"
                summary += f"   Suggested Specialty: {pattern.suggested_specialty.split('/')[0].strip()}\n\n"
        
        # Risk assessment
        summary += "**RISK ASSESSMENT:**\n"
        summary += f"Calculated Risk Score: {risk_score}/100\n"
        summary += f"Severity Level: {severity.value}\n\n"
        
        # Clinical recommendations
        summary += "**CLINICAL RECOMMENDATIONS:**\n"
        
        if severity == SeverityLevel.NORMAL:
            summary += "• Continue routine health maintenance\n"
            summary += "• No immediate intervention required\n"
        elif severity == SeverityLevel.LOW:
            summary += "• Schedule routine follow-up with primary care physician\n"
            summary += "• Consider lifestyle modifications if applicable\n"
        elif severity == SeverityLevel.MODERATE:
            summary += "• Medical consultation recommended within 1-2 weeks\n"
            summary += "• Additional diagnostic workup may be warranted\n"
        elif severity == SeverityLevel.HIGH:
            summary += "• Prompt medical evaluation recommended within 2-3 days\n"
            summary += "• Further diagnostic testing likely required\n"
        else:  # CRITICAL
            summary += "⚠️ **URGENT: Immediate medical attention required**\n"
            summary += "• Contact healthcare provider immediately\n"
            summary += "• Consider emergency department evaluation if symptomatic\n"
        
        # Disclaimer
        summary += "\n" + "─" * 70 + "\n"
        summary += "**IMPORTANT NOTICE:**\n"
        summary += "This analysis is for informational purposes only and does not constitute\n"
        summary += "medical advice, diagnosis, or treatment. Please consult with a qualified\n"
        summary += "healthcare professional for proper medical evaluation and management.\n"
        
        return summary
    
    @staticmethod
    def _get_severity_arabic(severity: SeverityLevel) -> str:
        """Get Arabic translation for severity level"""
        severity_map = {
            SeverityLevel.NORMAL: "طبيعي",
            SeverityLevel.LOW: "منخفض",
            SeverityLevel.MODERATE: "متوسط",
            SeverityLevel.HIGH: "عالي",
            SeverityLevel.CRITICAL: "حرج"
        }
        return severity_map.get(severity, severity.value)
    
    @staticmethod
    def generate_clinical_significance(test_name: str, status: TestStatus) -> str:
        """
        Generate simple Arabic explanation for what the test means.
        """
        explanations = {
            "Hemoglobin": {
                "Low": "قد يعني أنيميا (فقر دم) - ممكن تحس بتعب وإرهاق",
                "High": "ممكن يكون بسبب جفاف أو مشاكل في التنفس"
            },
            "WBC": {
                "Low": "جهاز المناعة ضعيف - خلي بالك من العدوى",
                "High": "ممكن يكون فيه عدوى أو التهاب في الجسم"
            },
            "RBC": {
                "Low": "عدد كريات الدم الحمراء قليل - ممكن تحس بتعب",
                "High": "عدد كريات الدم الحمراء عالي - يحتاج تقييم"
            },
            "Platelets": {
                "Low": "خطر نزيف - خلي بالك من الجروح",
                "High": "ممكن خطر تجلط - يحتاج متابعة"
            },
            "MCV": {
                "Low": "كريات الدم صغيرة - غالباً نقص حديد",
                "High": "كريات الدم كبيرة - ممكن نقص فيتامين ب12"
            }
        }
        
        test_explanations = explanations.get(test_name, {})
        
        if status in [TestStatus.LOW, TestStatus.CRITICAL_LOW]:
            return test_explanations.get("Low", "يحتاج تقييم طبي")
        elif status in [TestStatus.HIGH, TestStatus.CRITICAL_HIGH]:
            return test_explanations.get("High", "يحتاج تقييم طبي")
        
        return "في المعدل الطبيعي"
