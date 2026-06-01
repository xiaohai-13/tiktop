# ============================================================
# FastAPI 主入口
# ============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="TikTok AI 智能运营系统",
    description="基于 DeepSeek 的 TikTok 竞品分析 & 内容策略引擎",
    version="0.1.0",
)

# CORS — 允许 Streamlit Dashboard 跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
