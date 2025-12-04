# from fastapi import APIRouter, Request
# import logging
# import json
# import asyncio
# from utils.agent import review_merge_request
# from utils.gitlab_api import get_mr_diff

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# router = APIRouter()

# async def _process_webhook_background(project_id, mr_iid, diff, source_branch):
#     """Background task to process the merge request review."""
#     try:
#         logger.info("=" * 80)
#         logger.info("Starting background merge request review...")
#         logger.info(f"Project ID: {project_id}, MR IID: {mr_iid}, Branch: {source_branch}")
#         print(f"Background task started for Project {project_id}, MR {mr_iid}")
        
#         # If diff is empty or too short, fetch it from GitLab API
#         if not diff or len(str(diff)) < 50:
#             logger.info("Diff is empty or too short, fetching from GitLab API...")
#             print("Fetching diff from GitLab API...")
#             diff = await get_mr_diff(project_id, mr_iid)
#             if diff:
#                 logger.info(f"Fetched diff from API, length: {len(diff)} characters")
#                 print(f"Fetched diff from API, length: {len(diff)} characters")
#             else:
#                 logger.warning("Could not fetch diff from GitLab API")
#                 print("Could not fetch diff from GitLab API")
        
#         await review_merge_request(project_id, mr_iid, diff, source_branch)
#         logger.info("Background merge request review completed successfully")
#         print("Background merge request review completed successfully")
#     except Exception as e:
#         logger.error("=" * 80)
#         logger.error(f"ERROR in background review task: {e}", exc_info=True)
#         print(f"ERROR in background review task: {e}")
#         import traceback
#         print(traceback.format_exc())

# @router.post("/webhook/gitlab")
# async def gitlab_webhook(request: Request):
#     # Log webhook hit immediately
#     logger.info("=" * 80)
#     logger.info("Webhook hit (minimal handler)")
#     logger.info("=" * 80)
#     print("Webhook hit (minimal handler)")
    
#     try:
#         payload = await request.json()
        
#         # Log full webhook payload
#         logger.info("WEBHOOK RECEIVED")
#         logger.info(f"Full payload: {json.dumps(payload, indent=2)}")
        
#         # Defensive parsing
#         project = payload.get("project") or {}
#         project_id = project.get("id")
#         obj = payload.get("object_attributes") or {}
#         mr_iid = obj.get("iid")
#         source_branch = obj.get("source_branch", "unknown")
#         target_branch = obj.get("target_branch", "unknown")
        
#         # Try to get diff from changes or object_attributes
#         # Note: GitLab webhooks typically don't include full diff, so we'll fetch it in background task
#         changes = payload.get("changes", {})
#         diff = changes.get("diff", {})
#         if isinstance(diff, dict):
#             diff = diff.get("current", diff.get("previous", ""))
#         if not diff or len(str(diff)) < 10:
#             # Try to get from object_attributes
#             diff = obj.get("last_commit", {}).get("message", "")
#             if not diff:
#                 diff = ""  # Will be fetched from API in background task
        
#         # Log extracted values
#         logger.info(f"Project ID: {project_id}")
#         logger.info(f"Merge Request IID: {mr_iid}")
#         logger.info(f"Source Branch: {source_branch}")
#         logger.info(f"Target Branch: {target_branch}")
#         logger.info(f"Diff data length: {len(str(diff))} characters")
#         logger.info(f"Diff preview: {str(diff)[:200]}...")
        
#         # Return immediately to avoid hanging
#         response = {"status": "ok"}
        
#         # Validate required fields
#         if not project_id or not mr_iid:
#             logger.error(f"Missing required fields - project_id: {project_id}, mr_iid: {mr_iid}")
#             return {"status": "ok", "message": "missing fields - review skipped"}
        
#         # Process the merge request review in background
#         logger.info("Scheduling background task for merge request review...")
#         asyncio.create_task(_process_webhook_background(project_id, mr_iid, diff, source_branch))
        
#         # Return immediately
#         logger.info("Returning immediate response to webhook caller")
#         return response
        
#     except json.JSONDecodeError as e:
#         logger.error(f"JSON decode error: {e}")
#         return {"status": "ok", "message": "Invalid JSON payload"}
#     except Exception as e:
#         logger.error(f"Error processing webhook: {e}", exc_info=True)
#         return {"status": "ok", "message": f"Error: {str(e)}"}

# @router.get("/test/webhook")
# async def test_webhook():
#     logger.info("Test webhook endpoint called")
#     return {"status": "success", "message": "webhook working"}

# @router.post("/test/webhook/manual")
# async def test_webhook_manual(request: Request):
#     """Manual test endpoint - accepts a JSON payload to test webhook processing."""
#     try:
#         payload = await request.json()
#         logger.info("Manual webhook test received")
#         print("Manual webhook test received")
        
#         # Extract same fields as real webhook
#         project = payload.get("project") or {}
#         project_id = project.get("id")
#         obj = payload.get("object_attributes") or {}
#         mr_iid = obj.get("iid")
        
#         if not project_id or not mr_iid:
#             return {
#                 "status": "error",
#                 "message": "Missing project_id or mr_iid",
#                 "received": {"project_id": project_id, "mr_iid": mr_iid}
#             }
        
#         # Trigger background task
#         source_branch = obj.get("source_branch", "main")
#         diff = ""
#         asyncio.create_task(_process_webhook_background(project_id, mr_iid, diff, source_branch))
        
#         return {
#             "status": "ok",
#             "message": "Background task scheduled",
#             "project_id": project_id,
#             "mr_iid": mr_iid
#         }
#     except Exception as e:
#         logger.error(f"Error in manual test: {e}", exc_info=True)
#         return {"status": "error", "message": str(e)}

from fastapi import APIRouter, Request
import logging
import json
import asyncio

# Import but DO NOT use them in minimal mode
from utils.agent import review_merge_request
from utils.gitlab_api import get_mr_diff

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# -----------------------------
# Temporary minimal fast handler
# -----------------------------
@router.post("/webhook/gitlab")
async def gitlab_webhook(request: Request):
    """TEMPORARY ultra-fast webhook handler for debugging."""
    logger.info("Webhook hit — minimal fast handler")
    print("Webhook hit — minimal fast handler")

    # Try reading JSON (safe)
    try:
        payload = await request.json()
        logger.info("Payload received (minimal)")
        print(str(payload)[:200])
    except Exception as e:
        logger.error(f"Could not parse payload: {e}")

    # DO NOT run background task
    # DO NOT fetch diff
    # DO NOT call AI
    # Just immediately respond fast

    return {"status": "ok"}


# -----------------------------
# KEEP your test endpoints
# -----------------------------
@router.get("/test/webhook")
async def test_webhook():
    logger.info("Test webhook endpoint called")
    return {"status": "success", "message": "webhook working"}


@router.post("/test/webhook/manual")
async def test_webhook_manual(request: Request):
    """Manual test endpoint - accepts a JSON payload to test webhook processing."""
    try:
        payload = await request.json()
        logger.info("Manual webhook test received")
        print("Manual webhook test received")

        project = payload.get("project") or {}
        project_id = project.get("id")
        obj = payload.get("object_attributes") or {}
        mr_iid = obj.get("iid")

        if not project_id or not mr_iid:
            return {
                "status": "error",
                "message": "Missing project_id or mr_iid",
                "received": {"project_id": project_id, "mr_iid": mr_iid}
            }

        # Do NOT call background stuff right now — debug mode.
        return {
            "status": "ok",
            "message": "Minimal mode active – background task NOT scheduled.",
            "project_id": project_id,
            "mr_iid": mr_iid
        }

    except Exception as e:
        logger.error(f"Error in manual test: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
