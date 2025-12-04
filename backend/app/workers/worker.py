from app.services.gitlab_client import get_mr_changes, post_mr_comment, trigger_pipeline_with_trigger_token
from app.services.analysis import analyze_mr
from app.db import SessionLocal
from app.models import MRAnalysis, Installation
import os, traceback

def lookup_installation_token(project_id):
    # Placeholder: picks first installation row matching the project.
    db = SessionLocal()
    try:
        inst = db.query(Installation).filter(Installation.project_id == project_id).first()
        if inst:
            return inst.access_token
        return None
    finally:
        db.close()

def enqueue_mr_analysis(project_id, mr_iid):
    try:
        token = lookup_installation_token(project_id)
        if not token:
            # can't analyze without token - in production you should store per-project tokens
            print(f"No token found for project {project_id}. Install the agent for this project.")
            return
        mr = get_mr_changes(project_id, mr_iid, token)
        analysis = analyze_mr(mr)
        # Save summary to DB
        db = SessionLocal()
        try:
            record = MRAnalysis(project_id=project_id, mr_iid=mr_iid, summary_markdown=analysis["summary_markdown"], problems_json=str(analysis["problems"]), processed=True)
            db.add(record)
            db.commit()
        finally:
            db.close()
        # Post comment to MR
        post_mr_comment(project_id, mr_iid, analysis["summary_markdown"], token)
        # Optionally trigger pipeline automatically if env var and trigger token configured
        trigger_token = os.getenv("PIPELINE_TRIGGER_TOKEN")
        # simple heuristic: always trigger
        if trigger_token:
            ref = mr.get("target_branch", "master") if isinstance(mr, dict) else "master"
            try:
                trigger_pipeline_with_trigger_token(project_id, ref, trigger_token, variables={"AGENT_REVIEW": "true"})
            except Exception as e:
                print("Failed to trigger pipeline:", e)
    except Exception:
        traceback.print_exc()
