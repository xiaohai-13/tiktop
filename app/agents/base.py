# ============================================================
# Agent 基类 — DeepSeek 模型封装
# ============================================================
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from app.config import settings


def create_deepseek_llm(temperature: float = 0.7) -> ChatDeepSeek:
    """创建 DeepSeek Chat 模型实例"""
    if not settings.deepseek_configured:
        raise RuntimeError(
            "DeepSeek API Key 未配置。请在 .env 中设置 DEEPSEEK_API_KEY"
        )
    return ChatDeepSeek(
        model=settings.DEEPSEEK_MODEL,
        api_key=settings.DEEPSEEK_API_KEY,
        api_base=settings.DEEPSEEK_BASE_URL,
        temperature=temperature,
        max_tokens=4096,
    )


class TikTokAgent:
    """
    TikTok 运营 Agent 基类。
    封装了 LLM + 工具 + 记忆，子类只需定义 system_prompt 和 tools。
    """

    def __init__(self, name: str, system_prompt: str, tools: list | None = None):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = create_deepseek_llm()
        self.memory = MemorySaver()
        self.tools = tools or []

    def build_agent(self):
        """构建 LangGraph ReAct Agent"""
        return create_react_agent(
            model=self.llm,
            tools=self.tools,
            checkpointer=self.memory,
            prompt=self.system_prompt,
        )

    def run(self, user_input: str, thread_id: str = "default") -> str:
        """执行 Agent，返回最终响应"""
        agent = self.build_agent()
        config = {"configurable": {"thread_id": thread_id}}
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )
        # 提取最后一条 AI 消息
        messages = result.get("messages", [])
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.type == "ai":
                return msg.content
        return "（无响应）"
