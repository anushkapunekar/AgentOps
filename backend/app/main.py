import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, webhook, mr
from app.routers import install   # << new
from app.db import init_db

app = FastAPI(title="AgentOps - Code Review Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(webhook.router, prefix="/webhook")
app.include_router(mr.router, prefix="/mr")
app.include_router(install.router, prefix="/install")

@app.on_event("startup")
async def on_startup():
    init_db()
