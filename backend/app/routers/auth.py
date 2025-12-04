from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import os, requests, json, secrets
from urllib.parse import urlencode
from app.db import SessionLocal
from app.models import User

router = APIRouter()
GITLAB_BASE = os.getenv("GITLAB_BASE_URL", "https://gitlab.com")
CLIENT_ID = os.getenv("GITLAB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITLAB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GITLAB_OAUTH_REDIRECT_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

@router.get("/login")
def login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "api openid read_user"
    }
    url = f"{GITLAB_BASE}/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/callback")
def callback(code: str = None, error: str = None):
    if error:
        return RedirectResponse(f"{FRONTEND_URL}/connected?error=auth_error")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code from GitLab")
    token_url = f"{GITLAB_BASE}/oauth/token"
    resp = requests.post(token_url, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    })
    resp.raise_for_status()
    data = resp.json()
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    expires_in = data.get("expires_in")

    # get user info
    user_resp = requests.get(f"{GITLAB_BASE}/api/v4/user", headers={"Authorization": f"Bearer {access_token}"})
    user_resp.raise_for_status()
    user_info = user_resp.json()
    gitlab_user_id = user_info["id"]
    name = user_info.get("name")
    email = user_info.get("email")

    # create or update user in DB
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.gitlab_user_id == gitlab_user_id).first()
        if not user:
            user = User(gitlab_user_id=gitlab_user_id, name=name, email=email)
            db.add(user)
            db.commit()
            db.refresh(user)
        # update tokens & session
        user.access_token = access_token
        user.refresh_token = refresh_token
        user.token_expires_at = None
        user.name = name
        user.email = email
        user.session_token = secrets.token_urlsafe(32)
        db.add(user)
        db.commit()
        session_token = user.session_token
    finally:
        db.close()

    # Redirect to frontend with session token (frontend will store it)
    return RedirectResponse(f"{FRONTEND_URL}/connected?session_token={session_token}")
