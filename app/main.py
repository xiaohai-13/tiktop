# ============================================================
# FastAPI 主入口
# ============================================================
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="TikTok AI 智能运营系统",
    description="基于 DeepSeek 的 TikTok 竞品分析 & 内容策略引擎",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
from app.api.analysis import router as analysis_router
from app.api.webhook import router as webhook_router

app.include_router(analysis_router)
app.include_router(webhook_router)


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "version": "0.1.0",
        "deepseek_ready": settings.deepseek_configured,
        "feishu_ready": settings.feishu_configured,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.API_PORT, reload=True)
