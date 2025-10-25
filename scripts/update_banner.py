import requests, datetime, os

# 기본 정보
OWNER = "r3c-foundation"
REPO = "mesures-and-plan-0"
README_PATH = "README.md"
TOKEN = os.getenv("GH_TOKEN", None)

def get_traffic():
    """GitHub API로 트래픽 데이터 수집"""
    if not TOKEN:
        print("⚠️ GH_TOKEN not found; skipping traffic stats.")
        return {"views": 0, "clones": 0}

    headers = {"Authorization": f"token {TOKEN}"}
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/traffic/views"
    clones_url = f"https://api.github.com/repos/{OWNER}/{REPO}/traffic/clones"

    v = requests.get(url, headers=headers).json().get("count", 0)
    c = requests.get(clones_url, headers=headers).json().get("count", 0)
    return {"views": v, "clones": c}

def update_banner():
    stats = get_traffic()
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    banner = f"""
# 📊 mesures-and-plan-0

**Last Update:** {date}  
**Views (14d):** {stats['views']}  
**Clones (14d):** {stats['clones']}  

🧭 _Automated ecosystem tracker for R3C valuation & strategy._  
---
"""
    with open(README_PATH, "r", encoding="utf-8") as f:
        old = f.read().split("---")[-1]  # 기존 내용 유지
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(banner + old)

if __name__ == "__main__":
    update_banner()
