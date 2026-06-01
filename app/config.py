# ============================================================
# 全局配置管理
# ============================================================
import os
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent

# 加载 .env
load_dotenv(ROOT_DIR / ".env")


class Settings:
    # --- DeepSeek ---
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # --- 飞书 ---
    FEISHU_APP_ID: str = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET: str = os.getenv("FEISHU_APP_SECRET", "")
    FEISHU_VERIFY_TOKEN: str = os.getenv("FEISHU_VERIFY_TOKEN", "")
    FEISHU_ENCRYPT_KEY: str = os.getenv("FEISHU_ENCRYPT_KEY", "")

    # --- 服务端口 ---
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DASHBOARD_PORT: int = int(os.getenv("DASHBOARD_PORT", "8501"))

    # --- 数据库 ---
    SQLITE_PATH: str = os.getenv("SQLITE_PATH", str(ROOT_DIR / "data" / "tiktop.db"))
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", str(ROOT_DIR / "data" / "chroma"))

    # --- 其他 ---
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @property
    def deepseek_configured(self) -> bool:
        return bool(self.DEEPSEEK_API_KEY and "sk-your" not in self.DEEPSEEK_API_KEY)

    @property
    def feishu_configured(self) -> bool:
        return bool(self.FEISHU_APP_ID and "cli_" not in self.FEISHU_APP_ID)


settings = Settings()
