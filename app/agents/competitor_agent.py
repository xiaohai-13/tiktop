"""Competitor Analysis Agent - TikTok account deep analysis"""
import logging
from app.agents.base import TikTokAgent
from app.tools.tiktok_scraper import tiktok_scrape_profile

logger = logging.getLogger(__name__)

COMPETITOR_SYSTEM_PROMPT = """You are a TikTok competitive analysis expert.
Your job: analyze TikTok accounts using data collected by the tiktok_scrape_profile tool.

## Workflow
1. Call tiktok_scrape_profile(username) to get account data (followers, bio, recent videos)
2. Analyze the data deeply and produce a structured report

## Analysis Dimensions
- **Account Overview**: positioning, persona, target audience, niche
- **Data Performance**: follower scale, engagement rate, growth trajectory
- **Content Strategy**: video types, viral content patterns, posting cadence
- **Competitive Position**: strengths, weaknesses, differentiation opportunities
- **Actionable Recommendations**: 3-5 specific, data-backed suggestions

## Output Format
Output a well-structured Markdown report with:
1. Executive Summary (3-4 sentences)
2. Account Profile table
3. Content Analysis with patterns identified
4. Competitive Assessment
5. Recommended Actions (numbered list)

Be specific, data-driven, and actionable. Use Chinese for the report content.
"""


class CompetitorAgent(TikTokAgent):
    """Competitor analysis agent with data scraping + AI analysis"""

    def __init__(self, reasoning_effort: str = "high"):
        super().__init__(
            name="CompetitorAnalyzer",
            system_prompt=COMPETITOR_SYSTEM_PROMPT,
            tools=[tiktok_scrape_profile],
            reasoning_effort=reasoning_effort,
        )

    def analyze(self, username: str, thread_id: str | None = None) -> str:
        """Analyze a TikTok account and return a Markdown report"""
        prompt = (
            f"Please analyze TikTok account @{username}. "
            f"First use tiktok_scrape_profile to collect data, "
            f"then produce a comprehensive analysis report in Chinese."
        )
        thread = thread_id or f"competitor_{username}"
        logger.info(f"Starting analysis: @{username}")
        return self.run(prompt, thread_id=thread)
