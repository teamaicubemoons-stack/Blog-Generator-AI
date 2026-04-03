import os
from dotenv import load_dotenv

load_dotenv()

class CompanyAgent:
    def __init__(self):
        self.brand_voice = os.getenv("CUBEMOONS_BRAND_VOICE")
    
    def get_context(self):
        return {
            "name": "Cubemoons",
            "tone": "bold, strategic, magnetic",
            "voice": self.brand_voice,
            "core_services": [
                "AI Automation & Predictive Analytics",
                "Custom SaaS & Product Development",
                "Enterprise Web & Mobile Frameworks",
                "Digital Transformation Strategy",
                "Cloud Computing & Infrastructure"
            ],
            "industries": ["Healthcare", "EdTech", "E-commerce", "Real Estate", "Fintech"]
        }
