# TikTok AI 智能运营系统

基于 **DeepSeek** 大模型的 TikTok 竞品分析 & 内容策略引擎。

## 快速开始

### 1. 创建虚拟环境 & 安装依赖
 + "`" + 
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
 + "`" + 

### 2. 配置环境变量
 + "`" + 
cp .env.example .env
 + "`" + 
编辑 .env，填入 DeepSeek API Key 和飞书应用信息

### 3. 启动 API 服务
 + "`" + 
python -m app.main
 + "`" + 

### 4. 启动 Dashboard
 + "`" + 
streamlit run app/dashboard.py
 + "`" + 

## 技术栈

| 层面 | 选型 |
|------|------|
| LLM | DeepSeek (deepseek-chat) |
| AI 框架 | LangChain + LangGraph |
| API | FastAPI |
| Dashboard | Streamlit |
| 消息通道 | 飞书 Bot (lark-oapi) |
| 数据采集 | Playwright |
| 数据库 | SQLite + ChromaDB |
