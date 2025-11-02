# 🚀 Manus Agent - Quick Reference Card

## ⚡ Quick Start (5 Minutes)

### 1. Local Setup
```bash
git clone <your-repo>
cd manus-agent
chmod +x start.sh
./start.sh
```

### 2. Start Services
```bash
# Terminal 1
redis-server

# Terminal 2
uvicorn app.main:app --reload

# Terminal 3
celery -A app.workers.celery_app worker --loglevel=info
```

### 3. Access
- API: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## 🌐 Deploy to Render (10 Minutes)

### Quick Steps:
1. Push to GitHub
2. Render → New → Blueprint → Connect Repo
3. Add environment variables:
   - `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
   - `NEWS_API_KEY` (optional)
4. Click "Apply"
5. Wait ~5-10 minutes
6. Done! 🎉

### Verify:
```bash
curl https://your-app.onrender.com/health
```

---

## 📡 Essential API Calls

### Execute Agent Task
```bash
curl -X POST https://your-app.com/api/v1/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Fetch tech news", "context": {}}'
```

### Fetch News
```bash
curl -X POST https://your-app.com/api/v1/news/fetch?category=technology&limit=10
```

### Generate Content
```bash
curl -X POST https://your-app.com/api/v1/content/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI", "keywords": ["AI", "tech"]}'
```

### Create Project
```bash
curl -X POST https://your-app.com/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "domain": "example.com"}'
```

---

## 🔑 Required Environment Variables

```bash
# Minimum required:
OPENAI_API_KEY=sk-...          # OR
ANTHROPIC_API_KEY=sk-ant-...   # At least one required

SECRET_KEY=<generate-random>   # openssl rand -hex 32

# Auto-configured on Render:
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Optional but recommended:
NEWS_API_KEY=...
```

---

## 📁 Key Files

```
manus-agent/
├── app/main.py              # FastAPI app
├── app/config.py            # Settings
├── app/agents/
│   ├── orchestrator.py      # Main agent
│   ├── news_agent.py        # News ops
│   ├── seo_agent.py         # SEO ops
│   └── content_agent.py     # Content gen
├── app/api/routes.py        # API endpoints
├── requirements.txt         # Dependencies
├── render.yaml              # Deployment
├── .env.example             # Config template
├── README.md                # Full docs
├── DEPLOYMENT_GUIDE.md      # Deploy steps
└── PROJECT_OVERVIEW.md      # Architecture
```

---

## 🎯 Common Tasks

### Run Tests
```bash
pytest
pytest --cov=app
```

### Database Reset
```bash
python scripts/init_system.py
```

### View Logs (Render)
Dashboard → Your Service → Logs

### Update Deployment
```bash
git add .
git commit -m "Update"
git push origin main
# Auto-deploys on Render
```

### Scale Workers
Render Dashboard → manus-worker → Scale

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check Python 3.11+, requirements.txt |
| API 500 error | Check logs, verify API keys |
| Database error | Verify DATABASE_URL, restart service |
| News fetch fails | Check NEWS_API_KEY validity |
| Import errors | Set PYTHONPATH to project root |

---

## 📊 Architecture at a Glance

```
User Request → FastAPI → Orchestrator Agent
                              ↓
            ┌─────────────────┼─────────────────┐
            ↓                 ↓                  ↓
        News Agent       SEO Agent        Content Agent
            ↓                 ↓                  ↓
      [News Fetch]     [Web Scrape]      [LLM Service]
            ↓                 ↓                  ↓
        PostgreSQL ←────── Redis Cache
```

---

## 💡 Quick Examples

### Python SDK Usage
```python
from app.agents.orchestrator import OrchestratorAgent
from app.services.llm_service import LLMService

llm = LLMService()
orchestrator = OrchestratorAgent(llm)

result = await orchestrator.run(
    task="Fetch AI news and create article",
    project_context={"project_id": 1}
)
```

### Background Task
```python
from app.workers.celery_app import process_news_article

# Queue task
process_news_article.delay(article_id=123)
```

---

## 📚 Documentation

- **Full README**: README.md
- **Deployment**: DEPLOYMENT_GUIDE.md
- **Architecture**: PROJECT_OVERVIEW.md
- **API Docs**: https://your-app.com/docs

---

## 💰 Costs

**Render Hosting**: ~$28/month
**OpenAI API**: ~$20-50/month
**Total**: ~$50-80/month

Free tier available for testing!

---

## 🎓 Next Steps

1. ✅ Deploy to Render
2. ✅ Add API keys
3. ✅ Test endpoints
4. 🔄 Connect your domain
5. 🔄 Build frontend
6. 🔄 Add features

---

## 🆘 Help

- **Logs**: Render Dashboard
- **API Docs**: /docs endpoint
- **Health**: /health endpoint
- **Issues**: GitHub Issues

---

**Version**: 1.0.0  
**Status**: Production Ready ✅
