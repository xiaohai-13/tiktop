"""Account analysis service layer"""
import logging
from app.agents.competitor_agent import CompetitorAgent
from app.services.report_service import save_report

logger = logging.getLogger(__name__)

_competitor_agent: CompetitorAgent | None = None


def get_competitor_agent() -> CompetitorAgent:
    global _competitor_agent
    if _competitor_agent is None:
        _competitor_agent = CompetitorAgent()
    return _competitor_agent


def analyze_account(username: str) -> dict:
    """Analyze a TikTok account, auto-save report"""
    agent = get_competitor_agent()
    try:
        report = agent.analyze(username)
        save_report(username, report, report_type="competitor")
        return {"success": True, "username": username, "report": report}
    except Exception as e:
        logger.error(f"Analysis failed for @{username}: {e}")
        return {"success": False, "username": username, "error": str(e)}
