# TikTok AI

> DeepSeek V4 Pro  |  TikTok   |  LangChain + LangGraph

TikTok AI    —                                       

---

## Features

- ** ** —  TikTok     、  、  
- ** ** —           AI   
- ** ** —     、  
- ** ** —        
- **  Bot** —          

---

## Quick Start

### 1. Setup

```powershell
# Clone
git clone git@github.com:xiaohai-13/tiktop.git
cd tiktop

# Virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure

```powershell
copy .env.example .env
# Edit .env with your DeepSeek API key
# DEEPSEEK_API_KEY=sk-xxx
```

### 3. Run

```powershell
# Terminal 1: API server
python -m app.main
# -> http://localhost:8000/docs

# Terminal 2: Dashboard
streamlit run app/dashboard.py
# -> http://localhost:8501
```

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| LLM | DeepSeek V4 Pro (reasoning + thinking) |
| AI Framework | LangChain + LangGraph (ReAct Agent) |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | SQLite + ChromaDB |
| Scraping | Playwright (mock data mode available) |
| Messaging | Feishu Bot (lark-oapi) |

---

## Project Structure

```
tiktop/
├── app/
│   ├── main.py              # FastAPI entry (9 routes)
│   ├── config.py            # Settings (.env driven)
│   ├── dashboard.py         # Streamlit web UI
│   ├── agents/              # AI Agents
│   │   ├── base.py          # DeepSeek V4 Pro wrapper
│   │   ├── competitor_agent.py  # Account analysis
│   │   ├── content_agent.py     # Strategy generation
│   │   └── ops_agent.py         # Operations advice
│   ├── tools/               # Agent tools
│   │   └── tiktok_scraper.py    # Data scraper + mock
│   ├── channels/            # Messaging adapters
│   │   └── feishu_bot.py        # Feishu integration
│   ├── services/            # Business logic
│   ├── api/                 # REST API routes
│   └── db/                  # Database models
├── data/reports/            # Generated reports
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/analysis/account | Analyze TikTok account |
| GET | /api/analysis/account/{u} | Quick analysis |
| POST | /api/analysis/strategy | Content strategy |
| POST | /api/webhook/feishu | Feishu callback |
| GET | /api/reports | List reports |
| GET | /api/reports/{id} | Report detail |
| DELETE | /api/reports/{id} | Delete report |
| GET | /api/stats | Usage statistics |
| GET | /api/health | Health check |

---

## License

MIT
