import re
path = r"E:\agent-project\tiktop\app\tools\tiktok_scraper.py"
with open(path, encoding="utf-8") as f:
    content = f.read()

old = 'def tiktok_scrape_profile(username: str) -> str:\n    logger.info'
new = 'def tiktok_scrape_profile(username: str) -> str:\n    """Collect TikTok account public data including followers, bio, and recent videos. Parameter username: TikTok username without @ sign."""\n    logger.info'

content = content.replace(old, new)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Docstring fixed")
