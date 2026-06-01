"""Analysis API routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.account_service import analyze_account
from app.services.content_service import generate_content_strategy

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


class AnalyzeRequest(BaseModel):
    username: str
    depth: str = "basic"


class AnalyzeResponse(BaseModel):
    success: bool
    username: str
    report: str | None = None
    error: str | None = None


@router.post("/account", response_model=AnalyzeResponse)
async def analyze_single_account(req: AnalyzeRequest):
    if not req.username:
        raise HTTPException(status_code=400, detail="Username required")
    username = req.username.lstrip("@")
    result = analyze_account(username)
    return AnalyzeResponse(**result)


@router.get("/account/{username}")
async def quick_analyze(username: str):
    username = username.lstrip("@")
    return analyze_account(username)


class StrategyRequest(BaseModel):
    username: str

class StrategyResponse(BaseModel):
    success: bool
    username: str
    strategy: str | None = None
    error: str | None = None


@router.post("/strategy", response_model=StrategyResponse)
async def create_strategy(req: StrategyRequest):
    username = req.username.lstrip("@")
    result = generate_content_strategy(username)
    return StrategyResponse(**result)
