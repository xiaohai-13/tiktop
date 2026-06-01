from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from app.config import settings


def create_deepseek_llm(temperature: float = 0.7, reasoning_effort: str | None = None) -> ChatDeepSeek:
    if not settings.deepseek_configured:
        raise RuntimeError("DeepSeek API Key not configured")
    effort = reasoning_effort or settings.REASONING_EFFORT
    llm = ChatDeepSeek(
        model=settings.DEEPSEEK_MODEL,
        api_key=settings.DEEPSEEK_API_KEY,
        api_base=settings.DEEPSEEK_BASE_URL,
        temperature=temperature,
        max_tokens=8192,
        reasoning_effort=effort,
    )
    if settings.THINKING_ENABLED and hasattr(llm, "client"):
        try:
            llm.client.default_params = getattr(llm.client, "default_params", {}) or {}
            llm.client.default_params["extra_body"] = {"thinking": {"type": "enabled"}}
        except Exception:
            pass
    return llm


class TikTokAgent:
    def __init__(self, name: str, system_prompt: str, tools: list | None = None, reasoning_effort: str | None = None):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = create_deepseek_llm(reasoning_effort=reasoning_effort)
        self.memory = MemorySaver()
        self.tools = tools or []

    def build_agent(self):
        return create_react_agent(
            model=self.llm,
            tools=self.tools,
            checkpointer=self.memory,
            state_modifier=self.system_prompt,
        )

    def run(self, user_input: str, thread_id: str = "default") -> str:
        agent = self.build_agent()
        config = {"configurable": {"thread_id": thread_id}}
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )
        messages = result.get("messages", [])
        for msg in reversed(messages):
            if hasattr(msg, "content") and getattr(msg, "type", "") == "ai":
                return msg.content
        return "(no response)"
