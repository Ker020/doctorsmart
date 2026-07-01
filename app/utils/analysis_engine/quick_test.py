

import sys

import os
import json
from datetime import datetime

# Ensure current directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports
from analyzer import CBCAnalyzer
from analysis_result_models import SeverityLevel

print("=" * 70)
print("🔬 DR.SMART - Advanced CBC Lab Analysis Engine")
print("=" * 70)

# --------------------------------------------------
# Sample Lab Report (Simulated Upload)
# --------------------------------------------------

lab_text = """
AL NOOR LABORATORY
Patient Name: Ahmed Hassan
Age: 29 Years
Gender: Male

Hemoglobin (Hb): 10.5 g/dL Reference: 13.0 - 17.0
RBC Count: 3.8 x10^6/uL Reference: 4.5 - 5.9
WBC Count: 13.5 x10^3/uL Reference: 4.0 - 11.0
Platelets: 420 x10^3/uL Reference: 150 - 400
MCV: 72 fL Reference: 80 - 100
MCH: 24 pg Reference: 27 - 33
"""

print("\n📋 Starting medical analysis...")
print("-" * 70)

try:
    # Initialize Analyzer
    analyzer = CBCAnalyzer()

    # Run analysis
    result = analyzer.analyze(
        text=lab_text,
        age=29,
        gender="male",
        pregnant=False
    )

    print("\n✅ Analysis Completed Successfully!\n")

    # --------------------------------------------------
    # Risk Display
    # --------------------------------------------------
    print("📊 RISK ASSESSMENT")
    print(result.visual_risk)
    print(f"\nRisk Score: {result.risk_score}%")
    print(f"Severity Level: {result.severity_level.value}")

    # --------------------------------------------------
    # Detected Medical Patterns
    # --------------------------------------------------
    if result.detected_patterns:
        print("\n🧠 DETECTED MEDICAL PATTERNS")
        for i, pattern in enumerate(result.detected_patterns, 1):
            print(f"\n{i}. {pattern.condition}")
            print(f"   Arabic Name: {pattern.arabic_name}")
            print(f"   Confidence: {pattern.confidence:.0f}%")
            print(f"   Suggested Specialty: {pattern.suggested_specialty}")

            if pattern.supporting_findings:
                print("   Supporting Findings:")
                for finding in pattern.supporting_findings[:3]:
                    print(f"   • {finding}")

    # --------------------------------------------------
    # Abnormal Parameters
    # --------------------------------------------------
    if result.abnormal_parameters:
        print(f"\n⚠️ ABNORMAL PARAMETERS ({len(result.abnormal_parameters)})")

        for param in result.abnormal_parameters:
            print(f"\n• {param.test_name}: {param.value}")
            print(f"  Status: {param.status}")
            print(f"  Expected Range: {param.expected_range}")
            print(f"  Deviation: {param.deviation:.1f}%")
            print(f"  Clinical Note: {param.clinical_significance}")

    # --------------------------------------------------
    # Recommendations
    # --------------------------------------------------
    print("\n💊 RECOMMENDATIONS")
    for rec in result.recommendations:
        print(f"• {rec}")

    # --------------------------------------------------
    # Save Result to JSON File
    # --------------------------------------------------
    print("\n💾 Saving full structured result...")

    filename = f"cbc_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=4)

    print(f"📁 File saved successfully: {filename}")

    print("\n" + "=" * 70)
    print("🎉 DR.SMART Lab Engine Execution Finished")
    print("=" * 70)

except Exception as e:
    print("\n❌ ERROR DURING ANALYSIS")
    print(str(e))

from telegram_alert import send_telegram_alert

if result.risk_score >= 70:
    alert_message = f"""
🚨 DR.SMART High Risk Alert

Patient: {result.patient_summary.get('patient_name')}
Risk Score: {result.risk_score}%
Severity: {result.severity_level.value}

⚠️ Immediate medical attention recommended.
"""
    send_telegram_alert(alert_message)


