"""Content Strategy Agent - TikTok content planning"""
import logging
from app.agents.base import TikTokAgent
from app.tools.tiktok_scraper import tiktok_scrape_profile

logger = logging.getLogger(__name__)

CONTENT_SYSTEM_PROMPT = """You are a TikTok content strategy expert.
Your job: analyze an accounts data and produce actionable content strategy recommendations.

## Workflow
1. Call tiktok_scrape_profile(username) to collect account data
2. Analyze video patterns, engagement metrics, and audience signals
3. Generate specific, actionable content strategy

## Strategy Dimensions
- **Topic Selection**: identify high-potential content themes based on niche and trends
- **Video Structure**: hook scripts, content frameworks, CTAs
- **Posting Strategy**: optimal timing, frequency, hashtag strategy
- **Differentiation**: how to stand out from competitors in this niche

## Output Format
Output in Chinese, structured as:

1. **Content Positioning** (2-3 sentences)
2. **Recommended Content Pillars** (3-4 pillars with examples)
3. **Video Script Templates** (2-3 hook+structure examples)
4. **Posting Schedule** (best times, frequency)
5. **Hashtag Strategy** (primary + secondary tags)
6. **Growth Tactics** (3-5 specific tactics)

Be practical and specific - every suggestion should be something the creator can act on immediately.
"""


class ContentAgent(TikTokAgent):
    """Content strategy agent"""

    def __init__(self, reasoning_effort: str = "high"):
        super().__init__(
            name="ContentStrategist",
            system_prompt=CONTENT_SYSTEM_PROMPT,
            tools=[tiktok_scrape_profile],
            reasoning_effort=reasoning_effort,
        )

    def generate_strategy(self, username: str) -> str:
        prompt = (
            f"Generate a content strategy for TikTok account @{username}. "
            f"First use tiktok_scrape_profile to understand their current content, "
            f"then produce a complete strategy plan in Chinese."
        )
        logger.info(f"Generating strategy for @{username}")
        return self.run(prompt, thread_id=f"strategy_{username}")
