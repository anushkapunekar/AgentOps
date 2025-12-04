import os, requests, json

GITLAB_BASE = os.getenv("GITLAB_BASE_URL", "https://gitlab.com")

def api_get(path, token):
    url = f"{GITLAB_BASE}/api/v4{path}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def api_post(path, token, json_data=None, data=None):
    url = f"{GITLAB_BASE}/api/v4{path}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = requests.post(url, headers=headers, json=json_data, data=data)
    r.raise_for_status()
    # GitLab sometimes returns 201 with empty body for some endpoints - handle accordingly
    try:
        return r.json()
    except ValueError:
        return {"status_code": r.status_code}

def gitlab_list_projects(access_token, per_page=100):
    """
    List projects visible to the user (membership true)
    """
    page = 1
    projects = []
    while True:
        params = {"membership": "true", "per_page": per_page, "page": page}
        url = f"{GITLAB_BASE}/api/v4/projects"
        r = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, params=params)
        r.raise_for_status()
        res = r.json()
        if not res:
            break
        projects.extend(res)
        if len(res) < per_page:
            break
        page += 1
    return projects

def gitlab_create_project_hook(project_id, webhook_url, webhook_token, access_token):
    """
    Create a project hook for merge request events
    """
    path = f"/projects/{project_id}/hooks"
    payload = {
        "url": webhook_url,
        "token": webhook_token,
        "merge_requests_events": True,
        "enable_ssl_verification": True
    }
    return api_post(path, access_token, json_data=payload)

def gitlab_create_pipeline_trigger(project_id, access_token, description="AgentOps trigger"):
    """
    Create a pipeline trigger in project; requires maintainer privileges
    """
    path = f"/projects/{project_id}/triggers"
    payload = {"description": description}
    return api_post(path, access_token, json_data=payload)
