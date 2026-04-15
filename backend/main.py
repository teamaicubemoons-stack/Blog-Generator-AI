import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import diskcache as dc

# Agent Imports
from agents.trend_agent import TrendAgent
from agents.keyword_agent import KeywordAgent
from agents.company_agent import CompanyAgent
from agents.seo_planner import SEOPlannerAgent
from agents.blog_generator import BlogGeneratorAgent
from agents.seo_optimizer import SEOOptimizerAgent

app = FastAPI(title="AI Blogging Agent API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cache
cache = dc.Cache('./cache_db')

# Initialize Agents
trend_agent = TrendAgent()
keyword_agent = KeywordAgent()
company_agent = CompanyAgent()
seo_planner = SEOPlannerAgent()
blog_gen = BlogGeneratorAgent()
seo_opt = SEOOptimizerAgent()

class BlogRequest(BaseModel):
    topic: str

@app.post("/generate-blog")
async def start_pipeline(request: BlogRequest):
    topic = request.topic
    
    # Check Cache (Temporarily disabled for testing new prompt performance)
    # if topic in cache:
    #    return cache[topic]

    try:
        # Phase 1: Trend Analysis
        trends = trend_agent.analyze(topic)
        
        # Phase 2: Keyword Generation
        keywords_resp = keyword_agent.generate(trends, topic)
        keywords = json.loads(keywords_resp)
        
        # Phase 3: Company Context
        context = company_agent.get_context()
        
        # Phase 4: SEO Structure Planning
        structure_resp = seo_planner.plan(keywords, context, topic)
        structure = json.loads(structure_resp)
        
        # Phase 5: Blog Generation
        blog_content = blog_gen.generate_blog(structure, keywords, context)
        
        # Phase 6: SEO Optimization
        optimized_resp = seo_opt.optimize(blog_content)
        optimized = json.loads(optimized_resp)
        
        final_output = {
            "title": structure.get("SEO_Metadata", {}).get("Title"),
            "meta": structure.get("SEO_Metadata", {}).get("Meta_Description"),
            "content": optimized.get("final_blog"),
            "seo_score": optimized.get("seo_score"),
            "keywords": keywords,
            "status": "success"
        }
        
        # Save to Output Folder
        os.makedirs("outputs", exist_ok=True)
        filename = f"outputs/{topic.lower().replace(' ', '_')[:20]}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {final_output['title']}\n\n")
            f.write(f"**Meta:** {final_output['meta']}\n\n")
            f.write(f"**Keywords:** {json.dumps(final_output['keywords'])}\n\n")
            f.write(f"**SEO Score:** {final_output['seo_score']}%\n\n")
            f.write("---\n\n")
            f.write(final_output['content'])

        # Save to Cache
        cache.set(topic, final_output, expire=int(os.getenv("CACHE_TTL", 3600)))
        
        return final_output

    except Exception as e:
        print(f"Pipeline Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import subprocess
    import threading
    import time
    import webbrowser
    import sys

    def start_frontend():
        time.sleep(3)
        try:
            print("\n>>> Launching Frontend UI Silently...")
            subprocess.Popen(
                ["npm", "run", "dev"], 
                cwd="../frontend", 
                shell=True, 
                creationflags=0x08000000, # CREATE_NO_WINDOW
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(2)
            print(">>> Opening Browser...")
            webbrowser.open("http://localhost:5173")
        except Exception as e:
            print(f"Failed to auto-start frontend: {e}")

    try:
        # Start frontend in a separate thread
        threading.Thread(target=start_frontend, daemon=True).start()
        
        # Run uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
    except KeyboardInterrupt:
        print("\n>>> Shutting down gracefully...")
    finally:
        # Ensure we stay in the same terminal and exit cleanly
        print(">>> Server Stopped. Terminal is ready.")
