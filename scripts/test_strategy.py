import sys; sys.path.insert(0, r"E:\agent-project\tiktop")
from app.services.content_service import generate_content_strategy
print("Testing strategy generation...")
r = generate_content_strategy("mrbeast")
if r["success"]:
    print("SUCCESS:", len(r["strategy"]), "chars")
    print(r["strategy"][:400])
else:
    print("FAILED:", r.get("error"))
