# ============================================================
# Streamlit Dashboard — TikTok AI 运营系统
# ============================================================
import streamlit as st
import httpx

st.set_page_config(
    page_title="TikTok AI 运营系统",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000/api"


def call_api(endpoint: str, method: str = "GET", json_data: dict | None = None):
    """调用后端 API"""
    try:
        client = httpx.Client(timeout=60.0)
        if method == "POST":
            resp = client.post(f"{API_BASE}{endpoint}", json=json_data)
        else:
            resp = client.get(f"{API_BASE}{endpoint}")
        return resp.json() if resp.status_code == 200 else {"error": resp.text}
    except Exception as e:
        return {"error": f"无法连接到后端服务: {e}"}


# ---- 侧边栏 ----
st.sidebar.title("🎯 TikTok AI 运营系统")
st.sidebar.caption("DeepSeek · 智能竞品分析")

page = st.sidebar.radio(
    "导航",
    ["📊 系统概览", "🔍 竞品分析", "📈 内容策略", "📋 分析报告", "⚙️ 设置"],
)

# ---- 系统概览 ----
if page == "📊 系统概览":
    st.title("📊 系统概览")
    st.markdown("---")

    health = call_api("/health")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status = "🟢 在线" if health.get("status") == "ok" else "🔴 离线"
        st.metric("API 服务", status)
    with col2:
        ds_ready = "✅ 已配置" if health.get("deepseek_ready") else "⚠️ 待配置"
        st.metric("DeepSeek", ds_ready)
    with col3:
        fs_ready = "✅ 已配置" if health.get("feishu_ready") else "⚠️ 待配置"
        st.metric("飞书 Bot", fs_ready)
    with col4:
        st.metric("版本", health.get("version", "v0.1.0"))

    st.markdown("---")
    st.markdown("""
    ### 👋 欢迎使用 TikTok AI 智能运营系统

    **快速开始：**
    1. 在 ⚙️ 设置 中配置 DeepSeek API Key
    2. 进入 🔍 竞品分析，输入 TikTok 账号 ID
    3. AI 将自动采集数据并生成分析报告

    **核心能力：**
    - 🕵️ 竞品账号深度分析
    - 📊 内容策略智能建议
    - 🤖 飞书/微信机器人交互
    - 📝 自动生成分析报告
    """)

# ---- 竞品分析 ----
elif page == "🔍 竞品分析":
    st.title("🔍 竞品分析")
    st.markdown("---")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("输入分析目标")
        tiktok_username = st.text_input(
            "TikTok 账号 ID",
            placeholder="如 tiktok（不带 @）",
            help="输入要分析的 TikTok 用户名",
        )
        analyze_btn = st.button("🚀 开始分析", type="primary", use_container_width=True)

    with col_right:
        st.subheader("分析结果")

        if analyze_btn and tiktok_username:
            with st.spinner(f"正在分析 @{tiktok_username}，请稍候..."):
                result = call_api(
                    "/analysis/account",
                    method="POST",
                    json_data={"username": tiktok_username, "depth": "basic"},
                )

            if result.get("error"):
                st.error(f"分析失败: {result['error']}")
            elif result.get("success"):
                st.success(f"✅ @{tiktok_username} 分析完成")
                st.markdown(result.get("report", "*暂无报告内容*"))
            else:
                st.warning("分析结果异常，请检查后端日志")

# ---- 内容策略 ----
elif page == "📈 内容策略":
    st.title("📈 内容策略生成")
    st.markdown("---")
    st.info("🚧 内容策略功能开发中。完成竞品分析后将自动生成策略建议。")

# ---- 分析报告 ----
elif page == "📋 分析报告":
    st.title("📋 分析报告")
    st.markdown("---")
    st.info("🚧 报告管理功能开发中。分析完成后可在此查看和导出报告。")

# ---- 设置 ----
elif page == "⚙️ 设置":
    st.title("⚙️ 设置")
    st.markdown("---")

    from app.config import settings

    st.subheader("🔑 DeepSeek API 配置")
    api_key = st.text_input(
        "API Key",
        type="password",
        value="已配置 ✅" if settings.deepseek_configured else "",
        placeholder="sk-...",
    )
    st.caption(f"当前模型: {settings.DEEPSEEK_MODEL}")

    st.subheader("📱 飞书应用配置")
    feishu_id = st.text_input(
        "App ID",
        value="已配置 ✅" if settings.feishu_configured else "",
        placeholder="cli_...",
    )
    feishu_secret = st.text_input("App Secret", type="password", placeholder="...")

    if st.button("💾 保存配置", type="primary"):
        st.info("配置请直接编辑项目根目录的 .env 文件")
        st.code(open(".env.example", encoding="utf-8").read(), language="bash")

