from fastapi import APIRouter
from routes import example, webhook, status

api_router = APIRouter()

# Include route modules
api_router.include_router(example.router, prefix="/api", tags=["example"])
api_router.include_router(webhook.router, prefix="", tags=["webhook"])
api_router.include_router(status.router, prefix="", tags=["status"])

