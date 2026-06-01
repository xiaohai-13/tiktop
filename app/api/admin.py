"""Reports and admin API"""
from fastapi import APIRouter, HTTPException
from app.services.report_service import list_reports, get_report, delete_report
from app.db.models import get_session, AnalysisRecord

router = APIRouter(prefix="/api", tags=["reports"])


@router.get("/reports")
async def api_list_reports(type: str | None = None, limit: int = 20):
    reports = list_reports(report_type=type, limit=limit)
    return {"reports": reports, "count": len(reports)}


@router.get("/reports/{report_id}")
async def api_get_report(report_id: str):
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.delete("/reports/{report_id}")
async def api_delete_report(report_id: str):
    ok = delete_report(report_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"deleted": True, "id": report_id}


@router.get("/stats")
async def api_stats():
    session = get_session()
    total = session.query(AnalysisRecord).count()
    competitor = session.query(AnalysisRecord).filter_by(analysis_type="competitor").count()
    strategy = session.query(AnalysisRecord).filter_by(analysis_type="strategy").count()
    failed = session.query(AnalysisRecord).filter_by(status="failed").count()
    session.close()
    return {
        "total_analyses": total,
        "competitor_analyses": competitor,
        "strategy_analyses": strategy,
        "failed": failed,
    }
