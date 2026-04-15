import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class SEOPlannerAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def plan(self, keywords: dict, company_context: dict, topic: str):
        prompt = f"""
        Based on the topic '{topic}', the following keywords: {keywords}, and company context: {company_context}.
        
        Create a concentrated, high-authority SEO blueprint for a 1,500-word 'Executive Guide'. 
        The goal is to eliminate fluff and maximize "Insight Density".

        Structure Requirements:
        - "SEO_Metadata": {{ "Title": "...", "Focus_Keyword": "...", "Meta_Description": "..." }}
        - "Author_Byline": "..."
        - "Refined_Hook": "1-2 sentence emotional + business-impact manifesto."
        - "The_Killer_Stat_Analysis": "..."
        - "External_Authority_Signal": "Integrate 1-2 real insights from Gartner/McKinsey naturally."
        - "Industry_Reports": [ {{ "Industry": "...", "Challenge": "...", "Blueprint": "...", "Storytelling": "...", "Pro_Tip": "...", "Expert_Insight_Layer": "..." }} ]
        - "Micro_Engagement_Takeaway": "A bold, one-sentence strategic insight or takeaway statement."
        - "Visual_Briefs": "Descriptive narrative explaining visual ROI impact."
        - "Trend_Analysis_2026": "..."
        - "Conversion_Stack": {{ "Mid_CTA": "...", "Final_CTA": "...", "Subtle_Lead_Magnet": "..." }}
        - "Strategic_Blueprint_5_Steps": "..."
        - "Expert_FAQ": [ {{ "Question": "...", "Answer": "Expert-level with real-world examples" }} ]
        - "JSON_LD_Schema": "..."
        - "Final_Paradigm_Shift": "..."
        
        ### 9.7+ AUTHORITY RULES:
        - CREDIBILITY: Use soft qualifiers (e.g., "based on internal tracking", "in representative cases") for aggressive ROI stats. Avoid "fake" 300%+ claims unless sourced.
        - BRAND BALANCE: Limit company name mentions. Use a "Thought Leadership" tone that focuses on the solution rather than the vendor.
        - PHRASE VARIATION: Rotate terms: "Intelligent Workflows", "Automation Frameworks", "Smart Process Systems", "Autonomous Orchestration".
        - EXTERNAL SIGNALS: Mandate at least one external reference to an enterprise authority (Gartner, McKinsey, HBR).
        - HOOK: Must be 1-2 lines, urgent, and emotionally grounded in business risk or opportunity.
        ### IMPORTANT:
        - YOUR ENTIRE RESPONSE MUST BE A VALID JSON OBJECT.
        - ALL VALUES MUST BE INDEPENDENT STRINGS/LISTS.
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a professional SEO strategist."}, {"role": "user", "content": prompt}],
            model="gpt-4o",
            response_format={"type": "json_object"}
        )
        return chat_completion.choices[0].message.content
