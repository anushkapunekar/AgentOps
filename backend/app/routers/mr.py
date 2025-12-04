from fastapi import APIRouter, HTTPException
from app.db import SessionLocal
from app.models import MRAnalysis

router = APIRouter()

@router.get("/overview")
def overview(limit: int = 20):
    db = SessionLocal()
    try:
        rows = db.query(MRAnalysis).order_by(MRAnalysis.created_at.desc()).limit(limit).all()
        res = []
        for r in rows:
            res.append({
                "project_id": r.project_id,
                "mr_iid": r.mr_iid,
                "summary": r.summary_markdown,
                "created_at": r.created_at,
                "processed": r.processed
            })
        return {"items": res}
    finally:
        db.close()
