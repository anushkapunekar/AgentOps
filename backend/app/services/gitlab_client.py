import os
import requests

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
    try:
        return r.json()
    except ValueError:
        return {"status_code": r.status_code}


# ---------------------------------------------------------
# REQUIRED FUNCTION: get_mr_changes  (MISSING IN YOUR ERROR)
# ---------------------------------------------------------
def get_mr_changes(project_id, mr_iid, token):
    """
    Fetch all diffs / changes for a merge request.
    """
    path = f"/projects/{project_id}/merge_requests/{mr_iid}/changes"
    return api_get(path, token)


def post_mr_comment(project_id, mr_iid, body_markdown, token):
    path = f"/projects/{project_id}/merge_requests/{mr_iid}/notes"
    return api_post(path, token, json_data={"body": body_markdown})


# ---------------------------------------------------------
# For auto-install system
# ---------------------------------------------------------
def gitlab_list_projects(access_token, per_page=100):
    page = 1
    projects = []
    while True:
        url = f"{GITLAB_BASE}/api/v4/projects"
        params = {"membership": "true", "per_page": per_page, "page": page}

        r = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, params=params)
        r.raise_for_status()
        data = r.json()

        if not data:
            break

        projects.extend(data)

        if len(data) < per_page:
            break
        page += 1

    return projects


def gitlab_create_project_hook(project_id, webhook_url, webhook_token, access_token):
    """
    Create webhook for merge request events.
    """
    path = f"/projects/{project_id}/hooks"
    data = {
        "url": webhook_url,
        "token": webhook_token,
        "merge_requests_events": True,
        "enable_ssl_verification": True
    }
    return api_post(path, access_token, json_data=data)


def gitlab_create_pipeline_trigger(project_id, access_token, description="AgentOps Trigger"):
    """
    Create a new pipeline trigger token for this project.
    """
    path = f"/projects/{project_id}/triggers"
    return api_post(path, access_token, json_data={"description": description})


# ---------------------------------------------------------
# Legacy support (optional)
# ---------------------------------------------------------
def trigger_pipeline_with_trigger_token(project_id, ref, trigger_token, variables=None):
    """
    Trigger pipeline using project-level trigger token.
    """
    url = f"{GITLAB_BASE}/api/v4/projects/{project_id}/trigger/pipeline"
    data = {"ref": ref, "token": trigger_token}

    if variables:
        for key, val in variables.items():
            data[f"variables[{key}]"] = val

    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()
