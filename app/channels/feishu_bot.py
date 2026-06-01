# ============================================================
# 飞书 Bot — 消息处理 + 卡片回复
# ============================================================
import json
import logging
import lark_oapi as lark
from app.config import settings
from app.services.account_service import analyze_account

logger = logging.getLogger(__name__)


class FeishuBot:
    """飞书机器人 — 接收消息、意图识别、调用 Agent、回复卡片"""

    def __init__(self):
        self.app_id = settings.FEISHU_APP_ID
        self.app_secret = settings.FEISHU_APP_SECRET
        self.client = None
        if settings.feishu_configured:
            self.client = lark.Client.builder() \
                .app_id(self.app_id) \
                .app_secret(self.app_secret) \
                .build()

    def is_configured(self) -> bool:
        return self.client is not None

    # === URL 验证 ===
    def verify_url(self, body: dict) -> dict | None:
        """飞书事件订阅 URL 验证"""
        if body.get("type") == "url_verification":
            token = body.get("token", "")
            challenge = body.get("challenge", "")
            logger.info(f"URL 验证: token={token[:10]}...")
            return {"challenge": challenge}
        return None

    # === 事件处理 ===
    def handle_event(self, body: dict) -> dict:
        """处理飞书事件回调"""
        # URL 验证
        verify_resp = self.verify_url(body)
        if verify_resp:
            return verify_resp

        # 消息事件
        event = body.get("event", {})
        msg_type = event.get("message", {}).get("message_type", "")

        if msg_type == "text":
            return self._handle_text_message(event)

        logger.info(f"未处理的事件类型: {msg_type}")
        return {"code": 0}

    # === 文本消息处理 ===
    def _handle_text_message(self, event: dict) -> dict:
        """处理文本消息，意图识别 → 调用 Agent → 回复"""
        message = event.get("message", {})
        chat_id = message.get("chat_id", "")
        content_str = message.get("content", "{}")
        user_text = ""

        try:
            content = json.loads(content_str)
            user_text = content.get("text", "").strip()
        except json.JSONDecodeError:
            pass

        logger.info(f"收到消息: {user_text} (chat_id={chat_id})")

        # 简单意图识别
        reply = self._process_intent(user_text)

        # 回复消息
        self._reply_text(chat_id, reply)
        return {"code": 0}

    def _process_intent(self, text: str) -> str:
        """简单意图识别 + Agent 调度"""
        text_lower = text.lower().strip()

        # 分析账号
        if "分析" in text_lower or "analyze" in text_lower:
            import re
            # 提取可能的用户名: "分析 @xxx" / "分析 xxx"
            username = re.sub(r"(分析|analyze)\s*@?", "", text_lower).strip()
            if not username:
                return "请提供要分析的 TikTok 用户名，例如：分析 @tiktok"

            logger.info(f"触发竞品分析: @{username}")
            result = analyze_account(username)

            if result["success"]:
                return f"✅ 竞品分析完成: @{username}\n\n{result['report'][:3000]}"
            else:
                return f"❌ 分析失败: {result['error']}"

        # 帮助
        if text_lower in ["帮助", "help", "?", "？"]:
            return (
                "🎯 **TikTok AI 运营助手**\n\n"
                "支持以下指令：\n"
                "• **分析 @用户名** — 分析 TikTok 账号\n"
                "• **对比 @用户A @用户B** — 竞品对比（开发中）\n"
                "• **策略** — 内容策略建议（开发中）\n"
                "• **帮助** — 显示本消息"
            )

        # 默认回复
        return (
            "你好！我是 TikTok AI 运营助手 🤖\n\n"
            "我可以帮你：\n"
            "• **分析 @用户名** — 深度分析 TikTok 账号\n"
            "• **对比** — 竞品对比分析\n"
            f"• **帮助** — 查看所有指令\n\n"
            f"你刚才说: 「{text[:100]}」"
        )

    # === 消息发送 ===
    def _reply_text(self, chat_id: str, text: str):
        """发送文本回复"""
        if not self.client:
            logger.warning("飞书客户端未配置，无法发送回复")
            return

        try:
            content = json.dumps({"text": text})
            request = lark.im.v1.create_message.CreateMessageRequest.builder() \
                .receive_id_type("chat_id") \
                .request_body(
                    lark.im.v1.create_message.CreateMessageRequestBody.builder()
                    .receive_id(chat_id)
                    .msg_type("text")
                    .content(content)
                    .build()
                ).build()

            self.client.im.v1.message.create(request)
        except Exception as e:
            logger.error(f"飞书回复失败: {e}")

    # === 卡片消息（用于富文本报告） ===
    def send_card(self, chat_id: str, title: str, content: str):
        """发送卡片消息"""
        if not self.client:
            return

        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "blue",
            },
            "elements": [
                {"tag": "markdown", "content": content[:5000]},
            ],
        }

        try:
            request = lark.im.v1.create_message.CreateMessageRequest.builder() \
                .receive_id_type("chat_id") \
                .request_body(
                    lark.im.v1.create_message.CreateMessageRequestBody.builder()
                    .receive_id(chat_id)
                    .msg_type("interactive")
                    .content(json.dumps(card))
                    .build()
                ).build()

            self.client.im.v1.message.create(request)
        except Exception as e:
            logger.error(f"飞书卡片发送失败: {e}")


# 全局实例
feishu_bot = FeishuBot()

