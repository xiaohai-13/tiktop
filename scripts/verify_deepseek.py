# ============================================================
# DeepSeek 连接验证 & 基础能力测试
# ============================================================
import sys
from pathlib import Path

# 确保项目根目录在 sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.base import create_deepseek_llm
from app.config import settings


def test_deepseek_connection():
    """测试 DeepSeek API 连通性"""
    print("=" * 50)
    print("  TikTok AI 运营系统 — DeepSeek 验证")
    print("=" * 50)

    # 检查配置
    if not settings.deepseek_configured:
        print("\n[ERROR] DeepSeek API Key 未配置！")
        print("请复制 .env.example 为 .env，并填入你的 DEEPSEEK_API_KEY")
        return False

    print(f"\n[OK] 模型: {settings.DEEPSEEK_MODEL}")
    print(f"[OK] API 地址: {settings.DEEPSEEK_BASE_URL}")

    # 创建模型
    try:
        llm = create_deepseek_llm(temperature=0.3)
        print("\n[OK] ChatDeepSeek 实例创建成功")
    except Exception as e:
        print(f"\n[ERROR] 创建模型失败: {e}")
        return False

    # 发送测试消息
    test_prompt = "你好！请用一句话介绍你自己，然后告诉我你能否分析 TikTok 数据。"
    print(f"\n[TEST] 发送测试消息...")
    print(f"  Prompt: {test_prompt}")

    try:
        response = llm.invoke(test_prompt)
        print(f"\n[OK] DeepSeek 响应:")
        print(f"  {response.content}")
        print("\n" + "=" * 50)
        print("  验证通过！DeepSeek 已就绪。")
        return True
    except Exception as e:
        print(f"\n[ERROR] API 调用失败: {e}")
        return False


if __name__ == "__main__":
    success = test_deepseek_connection()
    sys.exit(0 if success else 1)
