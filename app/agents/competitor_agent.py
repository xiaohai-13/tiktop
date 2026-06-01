# ============================================================
# 竞品分析 Agent — 集成数据采集 + DeepSeek 分析
# ============================================================
import logging
from app.agents.base import TikTokAgent
from app.tools.tiktok_scraper import tiktok_scrape_profile

logger = logging.getLogger(__name__)

COMPETITOR_SYSTEM_PROMPT = """你是 TikTok 竞品分析专家。
用户会提供 TikTok 账号的用户名，你需要先用 tiktok_scrape_profile 工具采集数据，然后进行深度分析。

## 工作流程
1. 调用 tiktok_scrape_profile(username) 获取账号数据
2. 分析数据，从以下维度输出报告：

## 分析维度
- **账号概况**：定位、人设、目标受众
- **数据表现**：粉丝量级、互动率、增长趋势
- **内容策略**：视频类型分布、爆款特征、发布节奏
- **竞争优劣势**：差异化亮点、可改进点
- **运营建议**：可落地的 3-5 条具体建议

## 输出格式
请以结构化 Markdown 输出分析报告，使用表格和分点。
"""


class CompetitorAgent(TikTokAgent):
    """竞品分析 Agent — 采集数据 + AI 分析"""

    def __init__(self):
        super().__init__(
            name="CompetitorAnalyzer",
            system_prompt=COMPETITOR_SYSTEM_PROMPT,
            tools=[tiktok_scrape_profile],
        )

    def analyze(self, username: str, thread_id: str | None = None) -> str:
        """
        分析单个 TikTok 账号

        Args:
            username: TikTok 用户名（不带 @）
            thread_id: 会话 ID，用于记忆上下文

        Returns:
            Markdown 格式的分析报告
        """
        prompt = f"请分析 TikTok 账号 @{username}，先采集数据，然后给出完整分析报告。"
        thread = thread_id or f"competitor_{username}"
        logger.info(f"开始分析 @{username} (thread={thread})")
        return self.run(prompt, thread_id=thread)
