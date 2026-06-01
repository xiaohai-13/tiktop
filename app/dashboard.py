# ============================================================
# Streamlit Dashboard — TikTok AI 运营系统
# ============================================================
import streamlit as st
import requests

st.set_page_config(
    page_title="TikTok AI 运营系统",
    page_icon="🎯",
    layout="wide",
)

API_BASE = "http://localhost:8000/api"

# ---- 侧边栏 ----
st.sidebar.title("🎯 TikTok AI 运营系统")
st.sidebar.caption("基于 DeepSeek · 智能竞品分析")

page = st.sidebar.radio(
    "导航",
    ["📊 系统概览", "🔍 竞品分析", "📈 内容策略", "📋 分析报告", "⚙️ 设置"],
)

# ---- 系统概览 ----
if page == "📊 系统概览":
    st.title("📊 系统概览")
    st.markdown("---")

    # 尝试拉取后端健康状态
    try:
        resp = requests.get(f"{API_BASE}/health", timeout=3)
        health = resp.json()
    except Exception:
        health = {"status": "offline", "deepseek_ready": False, "feishu_ready": False}

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("API 服务", "🟢 在线" if health["status"] == "ok" else "🔴 离线")
    with col2:
        st.metric("DeepSeek", "✅ 已配置" if health.get("deepseek_ready") else "⚠️ 待配置")
    with col3:
        st.metric("飞书 Bot", "✅ 已配置" if health.get("feishu_ready") else "⚠️ 待配置")
    with col4:
        st.metric("版本", "v0.1.0")

    st.markdown("---")
    st.success("👋 欢迎使用 TikTok AI 智能运营系统！请先配置 DeepSeek API Key 和飞书应用。")

# ---- 竞品分析 ----
elif page == "🔍 竞品分析":
    st.title("🔍 竞品分析")
    st.markdown("---")
    st.info("🚧 竞品分析功能即将上线。请输入 TikTok 账号 ID 开始分析。")
    tiktok_username = st.text_input("TikTok 账号 ID（如 @tiktok）", placeholder="@username")
    if st.button("开始分析", type="primary") and tiktok_username:
        st.warning("功能开发中，敬请期待...")

# ---- 内容策略 ----
elif page == "📈 内容策略":
    st.title("📈 内容策略")
    st.markdown("---")
    st.info("🚧 内容策略生成功能即将上线。")

# ---- 分析报告 ----
elif page == "📋 分析报告":
    st.title("📋 分析报告")
    st.markdown("---")
    st.info("🚧 还没有生成过报告。先进行一次竞品分析吧！")

# ---- 设置 ----
elif page == "⚙️ 设置":
    st.title("⚙️ 设置")
    st.markdown("---")
    st.subheader("API 配置")
    st.text_input("DeepSeek API Key", type="password", placeholder="sk-...")
    st.text_input("飞书 App ID", placeholder="cli_...")
    st.text_input("飞书 App Secret", type="password", placeholder="...")
    if st.button("保存配置", type="primary"):
        st.success("配置已保存（需写入 .env 文件，功能开发中）")
