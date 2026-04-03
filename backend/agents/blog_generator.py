import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class BlogGeneratorAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_blog(self, structure: str, keywords: str, context: str):
        prompt = f"""
        Generate a 10/10, highly engaging, opinionated, and narrative-driven blog post based on this structure:
        {structure}
        
        Keywords to integrate naturally:
        {keywords}
        
        Brand Context (Cubemoons):
        {context}

        ### 9.7+/10 AUTHORITY PROTOCOL (SURGICAL):
        1. **SURGICAL HOOK**: 1-2 lines of high-impact, emotionally-charged manifesto focusing on business risk/opportunity. No generic openers.
        2. **CREDIBILITY & STATS**: Use soft qualifiers (e.g., "based on representative data" or "in typical scenarios") for ROI claims. Mandate at least ONE external link/reference to an enterprise authority (Gartner, McKinsey, HBR).
        3. **BRAND BALANCE**: Reduce repetitive company mentions. Transition to a "Thought Leadership" tone where the authority is the insight, not just the vendor.
        4. **LANGUAGE ROTATION**: Rotate technical terms naturally: "Intelligent Workflows," "Automation Frameworks," "Smart Process Systems," "Autonomous Orchestration."
        5. **MICRO TAKEAWAY**: Add ONE bold "Takeaway Statement" (Insight Box) that summarizes a strategic truth.
        6. **FAQ UPGRADE**: Every FAQ answer must be expert-level, concise (5 sentences), and include a specific strategic insight.
        7. **PRESERVATION**: Do NOT weaken metrics, case studies, or CTAs. Only polish the surrounding prose for a more premium, board-room ready feel.
        8. **VOLUME**: Maintain exactly 2,500 words of "Insight-Dense" depth.
        
        Format in clean, authoritative Markdown. No AI meta-text.
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return chat_completion.choices[0].message.content
