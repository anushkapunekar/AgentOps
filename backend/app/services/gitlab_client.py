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
        # Some GitLab endpoints return 201 with empty body
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
# Auto-install system helpers
# ---------------------------------------------------------
def gitlab_list_projects(access_token, per_page=100):
    """
    List all GitLab projects the user has membership in.
    """
    page = 1
    results = []

    while True:
        url = f"{GITLAB_BASE}/api/v4/projects"
        params = {
            "membership": "true",
            "per_page": per_page,
            "page": page
        }

        r = requests.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
            params=params
        )
        r.raise_for_status()
        batch = r.json()

        if not batch:
            break

        results.extend(batch)

        if len(batch) < per_page:
            break

        page += 1

    return results


def gitlab_create_project_hook(project_id, webhook_url, webhook_token, access_token):
    """
    Creates a webhook for merge requests.
    """
    path = f"/projects/{project_id}/hooks"

    payload = {
        "url": webhook_url,
        "token": webhook_token,
        "merge_requests_events": True,
        "enable_ssl_verification": True,
    }

    return api_post(path, access_token, json_data=payload)


def gitlab_create_pipeline_trigger(project_id, access_token, description="AgentOps Trigger"):
    """
    Creates a CI pipeline trigger token.
    """
    path = f"/projects/{project_id}/triggers"
    payload = {"description": description}
    return api_post(path, access_token, json_data=payload)


# ---------------------------------------------------------
# Optional legacy pipeline trigger
# ---------------------------------------------------------
def trigger_pipeline_with_trigger_token(project_id, ref, trigger_token, variables=None):
    """
    Trigger pipeline using trigger token.
    """
    url = f"{GITLAB_BASE}/api/v4/projects/{project_id}/trigger/pipeline"

    data = {
        "ref": ref,
        "token": trigger_token
    }

    if variables:
        for k, v in variables.items():
            data[f"variables[{k}]"] = v

    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()
