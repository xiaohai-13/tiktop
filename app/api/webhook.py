# ============================================================
# Webhook 路由 — 飞书事件回调
# ============================================================
from fastapi import APIRouter, Request
from app.channels.feishu_bot import feishu_bot

router = APIRouter(prefix="/api/webhook", tags=["webhook"])


@router.post("/feishu")
async def feishu_webhook(request: Request):
    """飞书事件回调入口"""
    body = await request.json()

    # 检查是否已配置
    if not feishu_bot.is_configured():
        return {"code": -1, "msg": "飞书未配置"}

    # 处理事件
    result = feishu_bot.handle_event(body)
    return result

