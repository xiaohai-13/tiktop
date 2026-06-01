"""TikTok AI Operations Dashboard - Streamlit"""
import streamlit as st
import httpx
import json
from datetime import datetime

st.set_page_config(page_title="TikTok AI", page_icon="", layout="wide", initial_sidebar_state="expanded")

API = "http://localhost:8000/api"

def api(method, path, json_data=None):
    try:
        client = httpx.Client(timeout=120.0)
        if method == "POST":
            r = client.post(f"{API}{path}", json=json_data)
        else:
            r = client.get(f"{API}{path}")
        return r.json() if r.status_code == 200 else {"error": r.text}
    except Exception as e:
        return {"error": str(e)}

# Sidebar
st.sidebar.title(" TikTok AI")
st.sidebar.caption("DeepSeek V4 Pro | Smart Analytics")
page = st.sidebar.radio("Menu", [" System Status", " Competitor Analysis", " Content Strategy", " Reports", " Settings"])

# Health
health = api("GET", "/health")

# === System Status ===
if page == " System Status":
    st.title("System Status")
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("API", "Online" if health.get("status") == "ok" else "Offline")
    c2.metric("DeepSeek V4", "Ready" if health.get("deepseek_ready") else "Not configured")
    c3.metric("Feishu", "Ready" if health.get("feishu_ready") else "Not configured")
    st.markdown("---")
    st.markdown("""
    ### How to use
    1. Enter a TikTok username in **Competitor Analysis**
    2. AI collects data and generates a deep analysis report
    3. View saved reports in **Reports**
    4. Get content strategy suggestions
    """)

# === Competitor Analysis ===
elif page == " Competitor Analysis":
    st.title("Competitor Analysis")
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Target Account")
        username = st.text_input("TikTok Username", placeholder="e.g. khaby.lame", help="Without @ sign")
        go = st.button(" Start Analysis", type="primary", use_container_width=True)
        st.caption("Examples: tiktok, khaby.lame, mrbeast, charlidamelio")
    with col2:
        st.subheader("Analysis Result")
        if go and username:
            with st.spinner(f"Analyzing @{username} with DeepSeek V4 Pro... This may take 30-60s"):
                result = api("POST", "/analysis/account", {"username": username, "depth": "deep"})
            if result.get("error"):
                st.error(f"Error: {result['error']}")
            elif result.get("success"):
                st.success(f"Analysis complete: @{username}")
                st.markdown(result.get("report", ""))
            else:
                st.warning("Unexpected response")

# === Content Strategy ===
elif page == " Content Strategy":
    st.title("Content Strategy")
    st.markdown("---")
    st.info("Enter a username above in Competitor Analysis first, then switch here for strategy suggestions.")
    strat_user = st.text_input("Username for strategy", placeholder="e.g. khaby.lame")
    if st.button("Generate Strategy", type="primary") and strat_user:
        with st.spinner("Analyzing content patterns..."):
            st.warning("Strategy generation coming soon. Run Competitor Analysis first!")

# === Reports ===
elif page == " Reports":
    st.title("Saved Reports")
    st.markdown("---")
    reports_resp = api("GET", "/reports?limit=20")
    reports = reports_resp.get("reports", [])
    if not reports:
        st.info("No reports yet. Run a Competitor Analysis first!")
    else:
        st.metric("Total Reports", len(reports))
        for r in reports:
            with st.expander(f" {r['username']} - {r.get('created_at','')[:16]} ({r.get('size_chars',0)} chars)"):
                detail = api("GET", f"/reports/{r['id']}")
                if detail.get("content"):
                    st.markdown(detail["content"][:5000])
                    if len(detail["content"]) > 5000:
                        st.caption("... (truncated, see full report in data/reports/)")
                if st.button(f"Delete", key=f"del_{r['id']}"):
                    api("DELETE", f"/reports/{r['id']}")
                    st.rerun()

# === Settings ===
elif page == " Settings":
    st.title("Settings")
    st.markdown("---")
    from app.config import settings
    st.subheader("DeepSeek V4 Pro")
    st.code(f"Model: {settings.DEEPSEEK_MODEL}\nReasoning: {settings.REASONING_EFFORT}\nThinking: {'On' if settings.THINKING_ENABLED else 'Off'}\nStatus: {'Configured' if settings.deepseek_configured else 'Not configured'}")
    st.subheader("Feishu Bot")
    st.code(f"App ID: {settings.FEISHU_APP_ID[:10]}...\nStatus: {'Configured' if settings.feishu_configured else 'Not configured'}")
    st.caption("Edit .env file to change settings")
