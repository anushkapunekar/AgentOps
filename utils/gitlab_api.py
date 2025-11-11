import os
import httpx
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Ensure we load the .env from the project root and override empty env vars
# Prefer explicit .env path relative to the repository root (parent of utils/)
_ENV_PATH = (Path(__file__).resolve().parents[1] / ".env")
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH, override=True)
else:
    # Fallback to searching upwards if direct path not found
    load_dotenv(find_dotenv(), override=True)

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} is not set")
    return value

async def post_comment_to_mr(project_id, mr_iid, comment):
    base_url = _require_env("BASE_URL")
    token = _require_env("GITLAB_TOKEN")
    url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/notes"
    headers = {"PRIVATE-TOKEN": token}
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json={"body": comment or ""})
        print("Comment posted:", r.status_code)
        return r.status_code

async def trigger_pipeline(project_id, ref):
    base_url = _require_env("BASE_URL")
    token = _require_env("GITLAB_TOKEN")
    url = f"{base_url}/projects/{project_id}/trigger/pipeline"
    headers = {"PRIVATE-TOKEN": token}
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json={"ref": ref})
        print("Pipeline trigger:", r.status_code)
        return r.status_code

