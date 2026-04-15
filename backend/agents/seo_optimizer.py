import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class SEOOptimizerAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def optimize(self, blog_content: str):
        prompt = f"""
        Analyze and optimize this blog for SEO, BUT PRESERVE its highly engaging, narrative-driven, and suspenseful tone.
        {blog_content}
        
        1. Improve keyword density naturally.
        2. Enhance readability WITHOUT making it sound like robotic AI or a generic corporate brochure. Keep the 1,500-word depth and the thrilling storytelling/narrative intact.
        3. Add an intriguing, non-generic FAQ section (minimum 4-5 questions with detailed answers).
        4. Provide suggestions for Internal Linking.
        5. Strengthen the Call-to-Action (CTA) to be magnetic, urgent, and tailored to booking an audit.
        6. **MANDATORY**: Do NOT summarize or shorten the blog. Maintain the full narrative span.
        7. Return JSON with the 'final_blog' in Markdown and 'seo_score' (out of 100).
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a professional SEO optimizer."}, {"role": "user", "content": prompt}],
            model="gpt-4o",
            response_format={"type": "json_object"}
        )
        return chat_completion.choices[0].message.content
