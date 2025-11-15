from fastapi import APIRouter, Request
import logging
import json
import asyncio
from utils.agent import review_merge_request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

async def _process_webhook_background(project_id, mr_iid, diff, source_branch):
    """Background task to process the merge request review."""
    try:
        logger.info("Starting background merge request review...")
        await review_merge_request(project_id, mr_iid, diff, source_branch)
        logger.info("Background merge request review completed successfully")
    except Exception as e:
        logger.error(f"Error in background review task: {e}", exc_info=True)

@router.post("/webhook/gitlab")
async def gitlab_webhook(request: Request):
    # Log webhook hit immediately
    logger.info("=" * 80)
    logger.info("Webhook hit")
    logger.info("=" * 80)
    print("Webhook hit")
    
    try:
        payload = await request.json()
        
        # Log full webhook payload
        logger.info("WEBHOOK RECEIVED")
        logger.info(f"Full payload: {json.dumps(payload, indent=2)}")
        
        # Defensive parsing
        project = payload.get("project") or {}
        project_id = project.get("id")
        obj = payload.get("object_attributes") or {}
        mr_iid = obj.get("iid")
        source_branch = obj.get("source_branch", "unknown")
        target_branch = obj.get("target_branch", "unknown")
        
        # Try to get diff from changes or object_attributes
        changes = payload.get("changes", {})
        diff = changes.get("diff", {})
        if isinstance(diff, dict):
            diff = diff.get("current", diff.get("previous", ""))
        if not diff:
            diff = obj.get("last_commit", {}).get("message", "")
        
        # Log extracted values
        logger.info(f"Project ID: {project_id}")
        logger.info(f"Merge Request IID: {mr_iid}")
        logger.info(f"Source Branch: {source_branch}")
        logger.info(f"Target Branch: {target_branch}")
        logger.info(f"Diff data length: {len(str(diff))} characters")
        logger.info(f"Diff preview: {str(diff)[:200]}...")
        
        # Return immediately to avoid hanging
        response = {"status": "ok"}
        
        # Validate required fields
        if not project_id or not mr_iid:
            logger.error(f"Missing required fields - project_id: {project_id}, mr_iid: {mr_iid}")
            return {"status": "ok", "message": "missing fields - review skipped"}
        
        # Process the merge request review in background
        logger.info("Scheduling background task for merge request review...")
        asyncio.create_task(_process_webhook_background(project_id, mr_iid, diff, source_branch))
        
        # Return immediately
        logger.info("Returning immediate response to webhook caller")
        return response
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return {"status": "ok", "message": "Invalid JSON payload"}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return {"status": "ok", "message": f"Error: {str(e)}"}

@router.get("/test/webhook")
async def test_webhook():
    logger.info("Test webhook endpoint called")
    return {"status": "success", "message": "webhook working"}
