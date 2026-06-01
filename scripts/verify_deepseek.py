# ============================================================
# DeepSeek V4 Pro ????
# ============================================================
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.base import create_deepseek_llm
from app.config import settings


def test_deepseek_connection():
    print("=" * 50)
    print("  TikTok AI - DeepSeek V4 Pro Verification")
    print("=" * 50)

    if not settings.deepseek_configured:
        print("\n[ERROR] DeepSeek API Key not configured!")
        return False

    print(f"\n[OK] Model: {settings.DEEPSEEK_MODEL}")
    print(f"[OK] Base URL: {settings.DEEPSEEK_BASE_URL}")
    print(f"[OK] Reasoning: {settings.REASONING_EFFORT}")
    print(f"[OK] Thinking: {'enabled' if settings.THINKING_ENABLED else 'disabled'}")

    try:
        llm = create_deepseek_llm(temperature=0.3)
        print("\n[OK] ChatDeepSeek instance created")
    except Exception as e:
        print(f"\n[ERROR] Failed to create model: {e}")
        return False

    test_prompt = "Hello! Please introduce yourself briefly in one sentence, and tell me you can analyze TikTok data."
    print(f"\n[TEST] Sending test message...")

    try:
        response = llm.invoke(test_prompt)
        content = response.content if hasattr(response, "content") else str(response)
        print(f"\n[OK] DeepSeek V4 Pro Response:")
        print(f"  {content}")
        print("\n" + "=" * 50)
        print("  Verification passed! DeepSeek V4 Pro is ready.")
        return True
    except Exception as e:
        print(f"\n[ERROR] API call failed: {e}")
        return False


if __name__ == "__main__":
    success = test_deepseek_connection()
    sys.exit(0 if success else 1)
