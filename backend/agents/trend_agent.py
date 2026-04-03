import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TrendAgent:
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.url = "https://google.serper.dev/search"

    def analyze(self, topic: str):
        payload = {
            "q": topic,
            "num": 5
        }
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(self.url, headers=headers, json=payload)
        data = response.json()
        
        results = {
            "competitor_titles": [res.get('title') for res in data.get('organic', [])],
            "organic_snippets": [res.get('snippet') for res in data.get('organic', [])],
            "people_also_ask": [res.get('question') for res in data.get('peopleAlsoAsk', [])],
            "related_searches": [res.get('query') for res in data.get('relatedSearches', [])]
        }
        return results
