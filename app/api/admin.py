# ============================================================
# 报告管理 API
# ============================================================
from fastapi import APIRouter, HTTPException
from app.services.report_service import list_reports, get_report, delete_report

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("")
async def api_list_reports(type: str | None = None, limit: int = 20):
    """获取报告列表"""
    reports = list_reports(report_type=type, limit=limit)
    return {"reports": reports, "count": len(reports)}


@router.get("/{report_id}")
async def api_get_report(report_id: str):
    """查看报告详情"""
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告未找到")
    return report


@router.delete("/{report_id}")
async def api_delete_report(report_id: str):
    """删除报告"""
    ok = delete_report(report_id)
    if not ok:
        raise HTTPException(status_code=404, detail="报告未找到")
    return {"deleted": True, "id": report_id}
