"""Content strategy service"""
import logging
from app.agents.content_agent import ContentAgent
from app.services.report_service import save_report

logger = logging.getLogger(__name__)
_agent = None

def get_content_agent():
    global _agent
    if _agent is None:
        _agent = ContentAgent()
    return _agent

def generate_content_strategy(username: str) -> dict:
    agent = get_content_agent()
    try:
        strategy = agent.generate_strategy(username)
        save_report(username, strategy, report_type="strategy")
        return {"success": True, "username": username, "strategy": strategy}
    except Exception as e:
        logger.error(f"Strategy failed for @{username}: {e}")
        return {"success": False, "username": username, "error": str(e)}
