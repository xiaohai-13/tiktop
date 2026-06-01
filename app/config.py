# ============================================================
# ??????
# ============================================================
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Settings:
    # --- DeepSeek ---
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")

    # --- DeepSeek V4 Pro reasoning ---
    REASONING_EFFORT: str = os.getenv("REASONING_EFFORT", "high")  # low | medium | high
    THINKING_ENABLED: bool = os.getenv("THINKING_ENABLED", "true").lower() == "true"

    # --- ?? ---
    FEISHU_APP_ID: str = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET: str = os.getenv("FEISHU_APP_SECRET", "")
    FEISHU_VERIFY_TOKEN: str = os.getenv("FEISHU_VERIFY_TOKEN", "")
    FEISHU_ENCRYPT_KEY: str = os.getenv("FEISHU_ENCRYPT_KEY", "")

    # --- ???? ---
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DASHBOARD_PORT: int = int(os.getenv("DASHBOARD_PORT", "8501"))

    # --- ??? ---
    SQLITE_PATH: str = os.getenv("SQLITE_PATH", str(ROOT_DIR / "data" / "tiktop.db"))
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", str(ROOT_DIR / "data" / "chroma"))

    # --- ?? ---
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @property
    def deepseek_configured(self) -> bool:
        return bool(self.DEEPSEEK_API_KEY and "sk-your" not in self.DEEPSEEK_API_KEY)

    @property
    def feishu_configured(self) -> bool:
        return bool(self.FEISHU_APP_ID and "cli_" not in self.FEISHU_APP_ID)


settings = Settings()
