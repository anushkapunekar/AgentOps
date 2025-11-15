from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
import os
import logging
from routes import webhook

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
env_path = find_dotenv()
if env_path:
    load_dotenv(env_path, override=True)
    logger.info(f"Loaded .env from: {env_path}")
else:
    # Fallback to explicit path
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path, override=True)
    logger.info(f"Loaded .env from: {env_path}")

app = FastAPI(
    title="AgentOps API",
    description="AI-powered code review service for GitLab merge requests",
    version="1.0.0"
)

# Include routers
app.include_router(webhook.router)

@app.get("/")
def root():
    """Root endpoint - health check."""
    return {"status": "running"}

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/health/env")
def env_status():
    """Check environment variable status."""
    base_url = os.getenv("BASE_URL")
    token = os.getenv("GITLAB_TOKEN")
    ai_model = os.getenv("AI_MODEL", "not set")
    has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
    
    return {
        "base_url": base_url,
        "has_token": bool(token),
        "ai_model": ai_model,
        "has_openai_key": has_openai_key
    }
