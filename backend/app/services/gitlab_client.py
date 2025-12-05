import os
import requests

# Base GitLab URL
GITLAB_BASE = os.getenv("GITLAB_BASE_URL", "https://gitlab.com")


# ---------------------------------------------------------
# Core API functions
# ---------------------------------------------------------
def api_get(path, token):
    """Generic GET request to GitLab API."""
    url = f"{GITLAB_BASE}/api/v4{path}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def api_post(path, token, json_data=None, data=None):
    """Generic POST request to GitLab API."""
    url = f"{GITLAB_BASE}/api/v4{path}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = requests.post(url, headers=headers, json=json_data, data=data)
    r.raise_for_status()

    try:
        return r.json()
    except ValueError:
        return {"status_code": r.status_code}


# ---------------------------------------------------------
# Merge Request functions
# ---------------------------------------------------------
def get_mr_changes(project_id, mr_iid, token):
    """
    Fetch the list of changed files & diffs for a merge request.
    """
    path = f"/projects/{project_id}/merge_requests/{mr_iid}/changes"
    return api_get(path, token)


def post_mr_comment(project_id, mr_iid, body_markdown, token):
    """
    Post a comment on a merge request.
    """
    path = f"/projects/{project_id}/merge_requests/{mr_iid}/notes"
    payload = {"body": body_markdown}
    return api_post(path, token, json_data=payload)


# ---------------------------------------------------------
# Auto-install system (listing projects, creating webhooks, creating triggers)
# ---------------------------------------------------------
def gitlab_list_projects(access_token, per_page=100):
    """
    List all GitLab projects the user has membership in.
    Used to display project list for "Install Agent".
    """
    page = 1
    projects = []

    while True:
        url = f"{GITLAB_BASE}/api/v4/projects"
        params = {
            "membership": "true",
            "per_page": per_page,
            "page": page
        }

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
    Creates a webhook on the GitLab project.
    Triggered for merge request events.
    """
    path = f"/projects/{project_id}/hooks"

    payload = {
        "url": webhook_url,
        "token": webhook_token,
        "merge_requests_events": True,
        "enable_ssl_verification": True
    }

    return api_post(path, access_token, json_data=payload)


def gitlab_create_pipeline_trigger(project_id, access_token, description="AgentOps Trigger"):
    """
    Creates a pipeline trigger token on the GitLab project.
    """
    path = f"/projects/{project_id}/triggers"
    payload = {"description": description}

    return api_post(path, access_token, json_data=payload)


# ---------------------------------------------------------
# Optional: trigger pipeline manually (legacy support)
# ---------------------------------------------------------
def trigger_pipeline_with_trigger_token(project_id, ref, trigger_token, variables=None):
    """
    Trigger a pipeline using the project trigger token.
    """
    url = f"{GITLAB_BASE}/api/v4/projects/{project_id}/trigger/pipeline"

    data = {
        "ref": ref,
