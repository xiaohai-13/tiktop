# ============================================================
# TikTok 数据采集工具 — 基于 Playwright
# ============================================================
import json
import re
import time
import logging
from typing import Optional
from dataclasses import dataclass, field, asdict

from playwright.sync_api import sync_playwright, Page
from langchain.tools import tool

logger = logging.getLogger(__name__)

# ============================================================
# 数据模型
# ============================================================

@dataclass
class TikTokProfile:
    """TikTok 账号资料"""
    username: str = ""
    nickname: str = ""
    bio: str = ""
    followers: int = 0
    following: int = 0
    likes: int = 0
    verified: bool = False
    avatar_url: str = ""
    profile_url: str = ""

@dataclass
class TikTokVideo:
    """单条视频信息"""
    video_id: str = ""
    description: str = ""
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    duration: str = ""
    upload_time: str = ""

@dataclass
class TikTokAnalysisData:
    """采集结果"""
    profile: TikTokProfile = field(default_factory=TikTokProfile)
    recent_videos: list[TikTokVideo] = field(default_factory=list)
    error: Optional[str] = None

# ============================================================
# 采集器
# ============================================================

def _parse_count(text: str) -> int:
    """解析 TikTok 的计数格式: '1.2M' → 1200000, '45.6K' → 45600"""
    if not text:
        return 0
    text = text.strip().replace(",", "")
    multiplier = 1
    if "M" in text or "m" in text:
        multiplier = 1_000_000
        text = text.replace("M", "").replace("m", "")
    elif "K" in text or "k" in text:
        multiplier = 1_000
        text = text.replace("K", "").replace("k", "")
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return 0


class TikTokScraper:
    """TikTok 数据采集器"""

    BASE_URL = "https://www.tiktok.com"

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser = None

    def _launch(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
            ],
        )

    def _close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def _new_page(self) -> Page:
        """创建新页面，设置反检测"""
        context = self.browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
        )
        page = context.new_page()
        # 隐藏 webdriver 特征
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
        """)
        return page

    def scrape_profile(self, username: str, max_videos: int = 10) -> TikTokAnalysisData:
        """采集单个账号的公开数据"""
        result = TikTokAnalysisData()
        profile_url = f"{self.BASE_URL}/@{username}"

        try:
            self._launch()
            page = self._new_page()

            logger.info(f"正在访问: {profile_url}")
            page.goto(profile_url, wait_until="domcontentloaded", timeout=30000)

            # 等待页面加载（TikTok 是 SPA）
            time.sleep(3)

            # ---- 提取资料信息 ----
            profile = TikTokProfile(username=username, profile_url=profile_url)
            self._extract_profile(page, profile)
            result.profile = profile

            # ---- 提取视频列表 ----
            videos = self._extract_videos(page, max_videos)
            result.recent_videos = videos

            logger.info(f"采集完成: @{username}, 粉丝={profile.followers}, 视频数={len(videos)}")

        except Exception as e:
            logger.error(f"采集失败: {e}")
            result.error = str(e)
        finally:
            self._close()

        return result

    def _extract_profile(self, page: Page, profile: TikTokProfile):
        """提取账号资料"""
        try:
            # 等待用户信息区域加载
            page.wait_for_selector('[data-e2e="user-title"]', timeout=10000)

            # 昵称
            try:
                el = page.locator('[data-e2e="user-title"]')
                if el.count() > 0:
                    profile.nickname = el.first.inner_text()
            except Exception:
                pass

            # 简介
            try:
                el = page.locator('[data-e2e="user-bio"]')
                if el.count() > 0:
                    profile.bio = el.first.inner_text()
            except Exception:
                pass

            # 粉丝 / 关注 / 点赞
            try:
                stats = page.locator('[data-e2e="user-info"] h3, [data-e2e="following"] strong')
                counts = stats.all_inner_texts()
                counts = [c.strip() for c in counts if c.strip()]

                # 通常顺序: Following, Followers, Likes
                if len(counts) >= 3:
                    profile.following = _parse_count(counts[0])
                    profile.followers = _parse_count(counts[1])
                    profile.likes = _parse_count(counts[2])
                elif len(counts) == 2:
                    profile.followers = _parse_count(counts[0])
                    profile.likes = _parse_count(counts[1])
            except Exception:
                pass

        except Exception as e:
            logger.warning(f"提取资料时出错: {e}")

    def _extract_videos(self, page: Page, max_count: int) -> list[TikTokVideo]:
        """提取最近视频列表"""
        videos = []
        try:
            # TikTok 视频卡片
            video_cards = page.locator('[data-e2e="user-post-item"]')
            count = min(video_cards.count(), max_count)

            for i in range(count):
                try:
                    card = video_cards.nth(i)
                    desc = ""
                    try:
                        desc_el = card.locator('[data-e2e="user-post-item-desc"]')
                        if desc_el.count() > 0:
                            desc = desc_el.first.inner_text()
                    except Exception:
                        pass

                    views = 0
                    try:
                        views_el = card.locator('[data-e2e="video-views"]')
                        if views_el.count() > 0:
                            views = _parse_count(views_el.first.inner_text())
                    except Exception:
                        pass

                    videos.append(TikTokVideo(description=desc[:200], views=views))
                except Exception:
                    continue

        except Exception as e:
            logger.warning(f"提取视频时出错: {e}")

        return videos


# ============================================================
# LangChain Tool 封装
# ============================================================

@tool
def tiktok_scrape_profile(username: str) -> str:
    """
    采集 TikTok 账号的公开数据，包括粉丝数、简介、近期视频等。
    参数 username: TikTok 用户名（不带 @，如 tiktok）
    返回 JSON 格式的分析数据
    """
    scraper = TikTokScraper(headless=True)
    data = scraper.scrape_profile(username)

    if data.error:
        return json.dumps({"error": data.error}, ensure_ascii=False)

    return json.dumps({
        "profile": asdict(data.profile),
        "recent_videos": [asdict(v) for v in data.recent_videos],
    }, ensure_ascii=False)


# ============================================================
# 独立测试入口
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 测试采集（需要 TikTok 可访问）
    test_user = input("请输入 TikTok 用户名 (不带 @): ").strip() or "tiktok"
    scraper = TikTokScraper(headless=False)
    result = scraper.scrape_profile(test_user, max_videos=5)

    print("\n" + "=" * 60)
    print(f"  TikTok 数据采集结果: @{test_user}")
    print("=" * 60)
    print(json.dumps({
        "profile": asdict(result.profile),
        "recent_videos": [asdict(v) for v in result.recent_videos],
        "error": result.error,
    }, ensure_ascii=False, indent=2))

