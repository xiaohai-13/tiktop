import sys
sys.path.insert(0, r"E:\agent-project\tiktop")
from app.services.account_service import analyze_account

print("Testing analysis pipeline with DeepSeek V4 Pro...")
result = analyze_account("khaby.lame")

if result["success"]:
    with open("data/reports/test_output.md", "w", encoding="utf-8") as f:
        f.write(result["report"])
    print(f"SUCCESS! Report saved: {len(result['report'])} chars")
    print("--- Preview ---")
    print(result["report"][:300])
else:
    print("FAILED:", result.get("error"))
