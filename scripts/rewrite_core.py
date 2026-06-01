"""Rewrite core module files with proper encoding"""
import os
ROOT = r"E:\agent-project\tiktop"

def write(relpath, content):
    full = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  OK: {relpath}")

# ============================================================
# tiktok_scraper.py
# ============================================================
SCRAPER = """# TikTok Data Scraper with Mock Data Support
import json, logging, random
from dataclasses import dataclass, field, asdict
from typing import Optional
from langchain.tools import tool

logger = logging.getLogger(__name__)


@dataclass
class TikTokProfile:
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
    profile: TikTokProfile = field(default_factory=TikTokProfile)
    recent_videos: list = field(default_factory=list)
    error: Optional[str] = None
    source: str = "mock"


# ============================================================
# Mock Data
# ============================================================

MOCK_PROFILES = {
    "tiktok": {
        "nickname": "TikTok Official",
        "bio": "The official TikTok account. Making every second count!",
        "followers": 67_800_000, "following": 142,
        "likes": 2_400_000_000, "verified": True,
    },
    "charlidamelio": {
        "nickname": "Charli D'Amelio",
        "bio": "dancing and stuff",
        "followers": 150_000_000, "following": 520,
        "likes": 11_500_000_000, "verified": True,
    },
    "khaby.lame": {
        "nickname": "Khabane Lame",
        "bio": "Simplicity is the key",
        "followers": 162_000_000, "following": 85,
        "likes": 2_800_000_000, "verified": True,
    },
    "mrbeast": {
        "nickname": "MrBeast",
        "bio": "I make expensive videos. Business inquiries only.",
        "followers": 105_000_000, "following": 23,
        "likes": 980_000_000, "verified": True,
    },
    "addisonre": {
        "nickname": "Addison Rae",
        "bio": "beauty and lifestyle creator",
        "followers": 88_000_000, "following": 390,
        "likes": 5_800_000_000, "verified": True,
    },
}

MOCK_VIDEOS = [
    {"desc": "POV: when you find the perfect sound", "views": 12_500_000, "likes": 2_100_000, "comments": 15400, "shares": 89000},
    {"desc": "Reply to user - here is the tutorial!", "views": 8_200_000, "likes": 1_500_000, "comments": 22100, "shares": 145000},
    {"desc": "Day in the life - what do you think?", "views": 5_100_000, "likes": 890_000, "comments": 8300, "shares": 34000},
    {"desc": "This trend is taking over!", "views": 15_800_000, "likes": 2_800_000, "comments": 31200, "shares": 210000},
    {"desc": "Behind the scenes of my latest project", "views": 3_400_000, "likes": 620_000, "comments": 5100, "shares": 18000},
    {"desc": "Which outfit is your favorite? 1 or 2?", "views": 9_700_000, "likes": 1_800_000, "comments": 45600, "shares": 67000},
    {"desc": "New upload! Check the link in bio", "views": 6_300_000, "likes": 1_100_000, "comments": 9800, "shares": 42000},
    {"desc": "Collaboration with creator - what next?", "views": 11_200_000, "likes": 2_300_000, "comments": 28900, "shares": 156000},
]


def generate_mock_data(username: str) -> TikTokAnalysisData:
    profile_data = MOCK_PROFILES.get(username.lower())
    if not profile_data:
        niches = ["Lifestyle", "Comedy", "Dance", "Beauty", "Tech", "Food"]
        profile_data = {
            "nickname": f"Creator @{username}",
            "bio": f"Content creator | {random.choice(niches)} niche",
            "followers": random.randint(10000, 5000000),
            "following": random.randint(50, 500),
            "likes": random.randint(100000, 500000000),
            "verified": random.random() > 0.8,
        }

    profile = TikTokProfile(
        username=username,
        nickname=profile_data["nickname"],
        bio=profile_data["bio"],
        followers=profile_data["followers"],
        following=profile_data["following"],
        likes=profile_data["likes"],
        verified=profile_data.get("verified", False),
        profile_url=f"https://www.tiktok.com/@{username}",
    )

    videos = []
    for i in range(random.randint(4, 8)):
        tpl = random.choice(MOCK_VIDEOS)
        videos.append(TikTokVideo(
            video_id=f"mock_{username}_{i}",
            description=tpl["desc"],
            views=random.randint(tpl["views"] // 2, int(tpl["views"] * 1.5)),
            likes=random.randint(tpl["likes"] // 2, int(tpl["likes"] * 1.5)),
            comments=random.randint(tpl["comments"] // 2, int(tpl["comments"] * 1.5)),
            shares=random.randint(tpl["shares"] // 2, int(tpl["shares"] * 1.5)),
            duration=f"{random.randint(15, 180)}s",
            upload_time=f"2026-0{random.randint(1,5)}-{random.randint(10,28)}",
        ))

    return TikTokAnalysisData(profile=profile, recent_videos=videos, source="mock")


# ============================================================
# LangChain Tool
# ============================================================

@tool
def tiktok_scrape_profile(username: str) -> str:
    logger.info(f"Scraping profile: @{username}")
    data = generate_mock_data(username)
    if data.error:
        return json.dumps({"error": data.error}, ensure_ascii=False)
    return json.dumps({
        "profile": asdict(data.profile),
        "recent_videos": [asdict(v) for v in data.recent_videos],
        "source": data.source,
    }, ensure_ascii=False)
"""

write("app/tools/tiktok_scraper.py", SCRAPER)

print("All files rewritten successfully!")
