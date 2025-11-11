import os
from fastapi import APIRouter
from dotenv import load_dotenv, find_dotenv

# Ensure .env is loaded similarly to utils
load_dotenv(find_dotenv(), override=True)

router = APIRouter()

@router.get("/health/env")
async def env_health():
    return {
        "base_url": os.getenv("BASE_URL"),
        "has_token": bool(os.getenv("GITLAB_TOKEN")),
    }

