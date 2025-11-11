from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
import os
from routes import webhook


#env_path = find_dotenv()
#print("🔍 Loading .env from:", env_path)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI()
app.include_router(webhook.router)

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health/env")
def env_status():
    base_url = os.getenv("BASE_URL")
    token = os.getenv("GITLAB_TOKEN")
    return {
        "base_url": base_url,
        "has_token": bool(token)
    }
