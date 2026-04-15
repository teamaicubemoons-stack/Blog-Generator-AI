import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class KeywordAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, trends_data: dict, topic: str):
        prompt = f"""
        Given the following trend data for the topic '{topic}':
        ### DATA INPUT:
        {trends_data}
        
        ### TASK:
        Analyze the search context and "People Also Ask" questions to identify:
        1. **High-Intent Primary Keywords**: Top terms users are searching for right now.
        2. **Semantic LSI Keywords**: Natural variations that prove topical authority.
        3. **Pain-Point Long-tail Keywords**: Specific search strings based on the "People Also Ask" questions (e.g., "how to fix...", "why is my...").

        ### OUTPUT:
        Respond strictly as a JSON object with keys: primary (list), secondary (list), long_tail (list).
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a keyword researcher."}, {"role": "user", "content": prompt}],
            model="gpt-4o",
            response_format={"type": "json_object"}
        )
        
        return chat_completion.choices[0].message.content
