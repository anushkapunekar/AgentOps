import os
import httpx
import logging
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_ENV_PATH = (Path(__file__).resolve().parents[1] / ".env")

# Load dotenv ONLY in local development to avoid overwriting Render env
if os.getenv("RENDER") is None:
    if _ENV_PATH.exists():
        load_dotenv(_ENV_PATH, override=True)
        logger.info(f"Loaded local .env from: {_ENV_PATH}")
    else:
        env_path = find_dotenv()
        load_dotenv(env_path, override=True)
        logger.info(f"Loaded .env from: {env_path}")
else:
    logger.info("Running on Render – NOT loading .env")

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        logger.error(f"Environment variable {name} is not set")
        raise ValueError(f"Environment variable {name} is not set")
    return value

async def get_mr_diff(project_id, mr_iid):
    try:
        base_url = _require_env("BASE_URL")
        token = _require_env("GITLAB_TOKEN")

        url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/changes"
        headers = {"PRIVATE-TOKEN": token}

        logger.info(f"Fetching MR diff: {url}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers)

        if r.status_code == 200:
            data = r.json()
            changes = data.get("changes", [])
            diff_text = "\n".join([c.get("diff", "") for c in changes])
            return diff_text

        logger.error(f"Failed diff request: {r.status_code} – {r.text[:200]}")
        return ""

    except Exception as e:
        logger.error(f"Error fetching MR diff: {e}", exc_info=True)
        return ""

async def post_comment_to_mr(project_id, mr_iid, comment):
    try:
        base_url = _require_env("BASE_URL")
        token = _require_env("GITLAB_TOKEN")

        url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/notes"
        headers = {"PRIVATE-TOKEN": token}
        payload = {"body": comment}

        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)

        return r.status_code

    except Exception as e:
        logger.error(f"Error posting comment: {e}", exc_info=True)
        return 0

async def trigger_pipeline(project_id, ref):
    try:
        base_url = _require_env("BASE_URL")
        token = _require_env("GITLAB_TOKEN")

        url = f"{base_url}/projects/{project_id}/pipeline"
        headers = {"PRIVATE-TOKEN": token}
        payload = {"ref": ref}

        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)

        return r.status_code

    except Exception as e:
        logger.error(f"Pipeline error: {e}", exc_info=True)
        return 0
