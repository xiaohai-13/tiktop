# ============================================================
# 账号分析服务层
# ============================================================
import logging
from app.agents.competitor_agent import CompetitorAgent

logger = logging.getLogger(__name__)

# 全局 Agent 实例（单例，复用 LLM 连接）
_competitor_agent: CompetitorAgent | None = None


def get_competitor_agent() -> CompetitorAgent:
    global _competitor_agent
    if _competitor_agent is None:
        _competitor_agent = CompetitorAgent()
    return _competitor_agent


def analyze_account(username: str) -> dict:
    """
    分析单个 TikTok 账号，返回结构化结果
    """
    agent = get_competitor_agent()
    try:
        report = agent.analyze(username)
        return {
            "success": True,
            "username": username,
            "report": report,
        }
    except Exception as e:
        logger.error(f"分析 @{username} 失败: {e}")
        return {
            "success": False,
            "username": username,
            "error": str(e),
        }
