from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

router = APIRouter()

class Settings(BaseModel):
    token: str
    base_url: str

@router.post("/save-settings")
async def save_settings(payload: dict):
    base_url = payload.get("base_url")
    token = payload.get("token")
    webhook_url = payload.get("webhook_url")

    os.environ["BASE_URL"] = base_url
    os.environ["GITLAB_TOKEN"] = token
    os.environ["WEBHOOK_URL"] = webhook_url

    return {"status": "saved"}


@router.post("/validate-token")
def validate_token(data: Settings):
    """
    Validate the user's GitLab token by calling the /user API.
    """
    base_url = data.base_url.rstrip("/")  # remove trailing slash if any
    url = f"{base_url}/api/v4/user"

    try:
        # GitLab PAT works with PRIVATE-TOKEN header
        headers = {"PRIVATE-TOKEN": data.token}
        resp = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Could not connect to GitLab.")

    if resp.status_code == 200:
        user = resp.json()
        return {
            "ok": True,
            "username": user.get("username"),
            "name": user.get("name"),
            "avatar_url": user.get("avatar_url"),
        }
    elif resp.status_code in (401, 403):
        raise HTTPException(status_code=400, detail="Invalid or unauthorized GitLab token.")
    else:
        raise HTTPException(
            status_code=400,
            detail=f"GitLab error: {resp.status_code} {resp.text[:200]}",
        )
@router.post("/list-repos")
def list_repos(data: Settings):
    base_url = data.base_url.rstrip("/")
    url = f"{base_url}/api/v4/projects"

    headers = {"PRIVATE-TOKEN": data.token}

    # We use membership=true to show repos the user has access to
    params = {
        "membership": "true",
        "per_page": 100
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Could not connect to GitLab.")

    if resp.status_code == 200:
        projects = resp.json()

        # Simplify output for frontend
        result = [
            {
                "id": p["id"],
                "name": p["name_with_namespace"],
                "path": p["path_with_namespace"],
                "web_url": p["web_url"],
                "avatar_url": p.get("avatar_url"),
            }
            for p in projects
        ]

        return {"ok": True, "projects": result}

    elif resp.status_code in (401, 403):
        raise HTTPException(status_code=400, detail="Invalid or unauthorized GitLab token.")
    else:
        raise HTTPException(
            status_code=400,
            detail=f"GitLab error: {resp.status_code} {resp.text[:200]}"
        )
@router.post("/create-webhook")
def create_webhook(data: dict):
    token = data["token"]
    base_url = data["base_url"].rstrip("/")
    project_id = data["project_id"]
    webhook_url = data["webhook_url"]

    # GitLab API endpoint for adding a webhook
    url = f"{base_url}/api/v4/projects/{project_id}/hooks"

    headers = {
        "PRIVATE-TOKEN": token,
        "Content-Type": "application/json"
    }

    # Minimum required payload for GitLab to accept the hook
    payload = {
        "url": webhook_url,
        "push_events":False,
        "merge_requests_events": True,
        "tag_push_events":False,
        "enable_ssl_verification":False
    }

    resp = requests.post(url, headers=headers, json=payload)

    # success
    if resp.status_code == 201:
        return {
            "ok": True,
            "message": "Webhook created!",
            "gitlab_response": resp.json()
        }

    # failure
    return {
        "ok": False,
        "status": resp.status_code,
        "message": resp.text
    }
