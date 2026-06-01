# ============================================================
# 分析接口 API
# ============================================================
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.account_service import analyze_account

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


class AnalyzeRequest(BaseModel):
    username: str
    depth: str = "basic"  # basic | deep


class AnalyzeResponse(BaseModel):
    success: bool
    username: str
    report: str | None = None
    error: str | None = None


@router.post("/account", response_model=AnalyzeResponse)
async def analyze_single_account(req: AnalyzeRequest):
    """分析单个 TikTok 账号"""
    if not req.username:
        raise HTTPException(status_code=400, detail="用户名不能为空")

    # 去掉可能带上的 @
    username = req.username.lstrip("@")

    result = analyze_account(username)
    return AnalyzeResponse(**result)


@router.get("/account/{username}")
async def quick_analyze(username: str):
    """快速分析（GET 方式）"""
    username = username.lstrip("@")
    result = analyze_account(username)
    return result
