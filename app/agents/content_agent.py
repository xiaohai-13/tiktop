from app.agents.base import TikTokAgent

CONTENT_SYSTEM_PROMPT = """你是 TikTok 内容策略专家。
根据竞品分析和目标赛道，为用户生成内容策略建议。

## 策略维度
1. **选题方向**：基于趋势和竞品空白点
2. **脚本框架**：开头钩子 + 内容结构 + 结尾引导
3. **发布策略**：最佳发布时间、频率、话题标签
4. **差异化定位**：如何在同类内容中脱颖而出
"""

class ContentAgent(TikTokAgent):
    def __init__(self):
        super().__init__(name="ContentStrategist", system_prompt=CONTENT_SYSTEM_PROMPT)
