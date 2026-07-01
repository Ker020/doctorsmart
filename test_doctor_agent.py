from app import create_app
from app.agents.doctor_agent import DoctorAgent
import json

app = create_app()
with app.app_context():
    print("Testing DoctorAgent.analyze...")
    try:
        result = DoctorAgent.analyze("A 45-year-old male with severe chest pain and short of breath for 2 hours.")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error during analysis: {e}")
