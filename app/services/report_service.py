# ============================================================
# 报告服务 — 保存、管理、导出分析报告
# ============================================================
import os
import json
import logging
from datetime import datetime
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

REPORTS_DIR = Path(settings.SQLITE_PATH).parent / "reports"
REPORTS_INDEX = REPORTS_DIR / "index.json"


def _ensure_dirs():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _load_index() -> list[dict]:
    _ensure_dirs()
    if REPORTS_INDEX.exists():
        try:
            return json.loads(REPORTS_INDEX.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def _save_index(index: list[dict]):
    _ensure_dirs()
    REPORTS_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def save_report(username: str, report_content: str, report_type: str = "competitor") -> dict:
    """保存分析报告，返回报告元数据"""
    _ensure_dirs()

    report_id = f"{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    filename = f"{report_id}.md"
    filepath = REPORTS_DIR / filename

    # 写入 Markdown 文件
    header = f"# TikTok 分析报告: @{username}\n\n> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n> 类型: {report_type}\n\n---\n\n"
    filepath.write_text(header + report_content, encoding="utf-8")

    # 更新索引
    meta = {
        "id": report_id,
        "username": username,
        "type": report_type,
        "filename": filename,
        "created_at": datetime.now().isoformat(),
        "size_chars": len(report_content),
    }
    index = _load_index()
    index.insert(0, meta)
    _save_index(index)

    logger.info(f"报告已保存: {report_id}")
    return meta


def list_reports(report_type: str | None = None, limit: int = 20) -> list[dict]:
    """列出所有报告"""
    index = _load_index()
    if report_type:
        index = [r for r in index if r["type"] == report_type]
    return index[:limit]


def get_report(report_id: str) -> dict | None:
    """获取单个报告"""
    index = _load_index()
    for r in index:
        if r["id"] == report_id:
            filepath = REPORTS_DIR / r["filename"]
            if filepath.exists():
                return {
                    **r,
                    "content": filepath.read_text(encoding="utf-8"),
                }
    return None


def delete_report(report_id: str) -> bool:
    """删除报告"""
    index = _load_index()
    for r in index:
        if r["id"] == report_id:
            filepath = REPORTS_DIR / r["filename"]
            if filepath.exists():
                os.remove(filepath)
            index.remove(r)
            _save_index(index)
            logger.info(f"报告已删除: {report_id}")
            return True
    return False
