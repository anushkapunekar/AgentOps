import os
import httpx
import logging
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure we load the .env from the project root and override empty env vars
# Prefer explicit .env path relative to the repository root (parent of utils/)
_ENV_PATH = (Path(__file__).resolve().parents[1] / ".env")
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH, override=True)
    logger.info(f"Loaded .env from: {_ENV_PATH}")
else:
    # Fallback to searching upwards if direct path not found
    env_path = find_dotenv()
    load_dotenv(env_path, override=True)
    logger.info(f"Loaded .env from: {env_path}")

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        logger.error(f"Environment variable {name} is not set")
        raise ValueError(f"Environment variable {name} is not set")
    return value

async def get_mr_diff(project_id, mr_iid):
    """
    Fetch the diff for a merge request from GitLab API.
    
    Endpoint: GET /projects/{project_id}/merge_requests/{mr_iid}/changes
    """
    try:
        base_url = _require_env("BASE_URL")
        token = _require_env("GITLAB_TOKEN")
        
        url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/changes"
        headers = {"PRIVATE-TOKEN": token}
        
        logger.info(f"Fetching MR diff - Project: {project_id}, MR: {mr_iid}")
        logger.info(f"URL: {url}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers)
            
            logger.info(f"MR diff GET response status: {r.status_code}")
            
            if r.status_code == 200:
                data = r.json()
                # GitLab returns changes with diff in the 'changes' array
                changes = data.get("changes", [])
                diff_text = "\n".join([change.get("diff", "") for change in changes])
                logger.info(f"Fetched diff with {len(changes)} file changes, total length: {len(diff_text)}")
                return diff_text
            else:
                logger.error(f"Failed to fetch MR diff. Status: {r.status_code}, Response: {r.text[:200]}")
                return ""
                
    except Exception as e:
        logger.error(f"Error fetching MR diff: {e}", exc_info=True)
        return ""

async def post_comment_to_mr(project_id, mr_iid, comment):
    """
    Post a comment to a GitLab merge request.
    
    Endpoint: POST /projects/{project_id}/merge_requests/{mr_iid}/notes
    """
    try:
        base_url = _require_env("BASE_URL")
        token = _require_env("GITLAB_TOKEN")
        
        url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/notes"
        headers = {"PRIVATE-TOKEN": token}
        payload = {"body": comment or ""}
        
        logger.info(f"Posting comment to MR - Project: {project_id}, MR: {mr_iid}")
        logger.info(f"URL: {url}")
        logger.info(f"Comment length: {len(comment)} characters")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            
            logger.info(f"Comment POST response status: {r.status_code}")
            logger.info(f"Response headers: {dict(r.headers)}")
            
            try:
                response_body = r.json()
                logger.info(f"Response body: {response_body}")
            except:
                response_text = r.text[:500]  # First 500 chars
                logger.info(f"Response text (preview): {response_text}")
            
            if r.status_code not in [200, 201]:
                logger.error(f"Failed to post comment. Status: {r.status_code}, Response: {r.text[:200]}")
            
            print(f"Comment posted: {r.status_code}")
            return r.status_code
            
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except httpx.TimeoutException:
        logger.error("Request timeout while posting comment")
        raise
    except httpx.RequestError as e:
        logger.error(f"Request error while posting comment: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error posting comment: {e}", exc_info=True)
        raise

async def trigger_pipeline(project_id, ref):
    """
    Trigger a GitLab pipeline.
    
    Endpoint: POST /projects/{project_id}/pipeline
    JSON: {"ref": "main"}
    """
    try:
        base_url = _require_env("BASE_URL")
        token = _require_env("GITLAB_TOKEN")
        
        url = f"{base_url}/projects/{project_id}/pipeline"
        headers = {"PRIVATE-TOKEN": token}
        payload = {"ref": ref}
        
        logger.info(f"Triggering pipeline - Project: {project_id}, Ref: {ref}")
        logger.info(f"URL: {url}")
        logger.info(f"Payload: {payload}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            
            logger.info(f"Pipeline trigger response status: {r.status_code}")
            logger.info(f"Response headers: {dict(r.headers)}")
            
            try:
                response_body = r.json()
                logger.info(f"Response body: {response_body}")
            except:
                response_text = r.text[:500]  # First 500 chars
                logger.info(f"Response text (preview): {response_text}")
            
            if r.status_code not in [200, 201]:
                logger.error(f"Failed to trigger pipeline. Status: {r.status_code}, Response: {r.text[:200]}")
            
            print(f"Pipeline trigger: {r.status_code}")
            return r.status_code
            
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except httpx.TimeoutException:
        logger.error("Request timeout while triggering pipeline")
        raise
    except httpx.RequestError as e:
        logger.error(f"Request error while triggering pipeline: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error triggering pipeline: {e}", exc_info=True)
        raise
