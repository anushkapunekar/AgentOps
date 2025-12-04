from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
import os
import logging
from routes import webhook
from routes import settings
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env ONLY in local development
if os.getenv("RENDER") is None:
    env_path = find_dotenv()
    if env_path:
        load_dotenv(env_path, override=True)
        logger.info(f"Loaded local .env from: {env_path}")
    else:
        logger.info("No local .env found.")
else:
    logger.info("Running on Render – NOT loading .env")

# Debug check
print("DEBUG: GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))

app = FastAPI(
    title="AgentOps API",
    description="AI-powered code review service for GitLab merge requests",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook.router)
app.include_router(settings.router)

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/env")
def env_status():
    return {
        "base_url": os.getenv("BASE_URL"),
        "has_token": bool(os.getenv("GITLAB_TOKEN")),
        "ai_model": os.getenv("AI_MODEL", "not set"),
        "has_groq": bool(os.getenv("GROQ_API_KEY")),
    }

print("--------------------------------------------------")
print("DEBUG: CHECKING ENVIRONMENT VARIABLES ON RENDER")
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
print("ALL ENV:", {k: v for k, v in os.environ.items()})
print("--------------------------------------------------")
