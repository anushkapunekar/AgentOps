from fastapi import APIRouter, Request, Header, HTTPException, BackgroundTasks
import os
import json
from app.workers.worker import enqueue_mr_analysis
from app.db import SessionLocal
from app.models import Installation

router = APIRouter()
# We still accept a fallback WEBHOOK_SECRET for older setups
GLOBAL_WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", None)

@router.post("/gitlab")
async def gitlab_webhook(request: Request, background_tasks: BackgroundTasks, x_gitlab_event: str = Header(None), x_gitlab_token: str = Header(None)):
    payload = await request.json()
    # Determine project id
    project = payload.get("project", {})
    project_id = project.get("id")

    # Validate secret: accept if matches per-project stored secret or global env secret
    valid = False
    if GLOBAL_WEBHOOK_SECRET and x_gitlab_token == GLOBAL_WEBHOOK_SECRET:
        valid = True
    else:
        # lookup installation
        db = SessionLocal()
        try:
            inst = db.query(Installation).filter(Installation.project_id == project_id).first()
            if inst and inst.webhook_token and x_gitlab_token == inst.webhook_token:
                valid = True
        finally:
            db.close()

    if not valid:
        raise HTTPException(status_code=403, detail="Invalid webhook token")

    # Process MR events only
    if x_gitlab_event and "Merge Request" in x_gitlab_event:
        obj = payload.get("object_attributes", {})
        mr_iid = obj.get("iid")
        background_tasks.add_task(enqueue_mr_analysis, project_id, mr_iid)
    return {"ok": True}
