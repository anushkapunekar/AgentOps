from fastapi import APIRouter, Request
import logging
from utils.agent import review_merge_request

router = APIRouter()

@router.post("/webhook/gitlab")
async def gitlab_webhook(request: Request):
    payload = await request.json()
    logging.warning(payload)   # <-- See full body in terminal

    # Defensive parsing
    project = payload.get("project") or {}
    project_id = project.get("id")
    obj = payload.get("object_attributes") or {}
    mr_iid = obj.get("iid")
    changes = payload.get("changes") or {}
    diff = changes.get("diff", "")

    if not project_id or not mr_iid:
        return {"status": "missing fields", "payload": payload}

    print("Webhook received ✅")
    print("Project ID:", project_id)
    print("Merge Request IID:", mr_iid)
    print("Diff data:", diff)

    await review_merge_request(project_id, mr_iid, diff)
    return {"status": "received"}
