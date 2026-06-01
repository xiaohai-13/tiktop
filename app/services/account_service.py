"""Account analysis service layer"""
import logging
from app.agents.competitor_agent import CompetitorAgent
from app.services.report_service import save_report
from app.db.models import AnalysisRecord, get_session

logger = logging.getLogger(__name__)
_agent: CompetitorAgent | None = None


def get_competitor_agent() -> CompetitorAgent:
    global _agent
    if _agent is None:
        _agent = CompetitorAgent()
    return _agent


def analyze_account(username: str) -> dict:
    agent = get_competitor_agent()
    try:
        report = agent.analyze(username)
        meta = save_report(username, report, report_type="competitor")

        # SQLite record
        session = get_session()
        record = AnalysisRecord(
            username=username,
            analysis_type="competitor",
            report_path=f"data/reports/{meta['filename']}",
            status="completed",
        )
        session.add(record)
        session.commit()
        session.close()

        return {"success": True, "username": username, "report": report}
    except Exception as e:
        logger.error(f"Analysis failed for @{username}: {e}")
        return {"success": False, "username": username, "error": str(e)}
