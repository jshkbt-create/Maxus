# 🤖 Manus Agent System - Project Overview

## 📊 Project Summary

**Name**: Manus Agent System  
**Purpose**: Multi-agent AI system for automated content management, news aggregation, and SEO optimization  
**Primary Use Case**: Managing breakings.news and domain portfolio  
**Tech Stack**: Python, FastAPI, LangGraph, OpenAI/Anthropic, PostgreSQL, Redis  
**Deployment**: Render.com (fully configured)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Manus Agent System                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                │
│  │   FastAPI    │────────▶│ Orchestrator │                │
│  │   REST API   │         │    Agent     │                │
│  └──────────────┘         └──────┬───────┘                │
│        │                          │                         │
│        │           ┌──────────────┴──────────────┐         │
│        │           │                              │         │
│        │      ┌────▼────┐  ┌─────▼─────┐  ┌────▼────┐    │
│        │      │  News   │  │    SEO    │  │ Content │    │
│        │      │  Agent  │  │   Agent   │  │  Agent  │    │
│        │      └────┬────┘  └─────┬─────┘  └────┬────┘    │
│        │           │             │              │         │
│  ┌─────▼───────────▼─────────────▼──────────────▼─────┐  │
│  │                  Tool Layer                          │  │
│  │  [News Fetch] [Web Scrape] [LLM Service] [SEO]     │  │
│  └──────────────────────────────────────────────────────┘  │
│        │                                                    │
│  ┌─────▼────────────────────────────────────────────────┐  │
│  │              Data Layer                              │  │
│  │  [PostgreSQL Database]  [Redis Cache]               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Background Services:                                       │
│  • Celery Workers (async tasks)                            │
│  • Cron Jobs (scheduled news fetching)                     │
│  • Prometheus Monitoring                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Core Features

### 1. **Intelligent Task Orchestration**
- Analyzes user requests using LLM
- Routes tasks to specialized agents
- Manages workflow and error handling
- Provides unified results

### 2. **News Automation**
- Fetches breaking news from multiple sources (NewsAPI, RSS feeds)
- Processes and enriches articles with AI
- Auto-categorizes and tags content
- Scheduled fetching every 30 minutes
- Stores in database for publishing

### 3. **Content Generation**
- Creates articles, blog posts, social media content
- SEO-optimized writing
- Multiple style support (news, blog, technical)
- Keyword integration
- Readability optimization

### 4. **SEO Optimization**
- Automated keyword research
- Meta tag generation
- Content analysis and optimization
- SEO scoring
- Competitive analysis

### 5. **Web Automation**
- Static page scraping (httpx)
- Dynamic page scraping (Playwright)
- Content extraction and cleaning
- Link analysis

---

## 📁 Complete File Structure

```
manus-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry
│   ├── config.py                    # Configuration management
│   │
│   ├── agents/                      # AI Agents
│   │   ├── __init__.py
│   │   ├── orchestrator.py          # Main coordinator agent
│   │   ├── news_agent.py            # News operations
│   │   ├── seo_agent.py             # SEO operations
│   │   └── content_agent.py         # Content generation
│   │
│   ├── api/                         # API Layer
│   │   ├── __init__.py
│   │   └── routes.py                # REST API endpoints
│   │
│   ├── db/                          # Database Layer
│   │   ├── __init__.py
│   │   └── database.py              # SQLAlchemy setup
│   │
│   ├── models/                      # Data Models
│   │   ├── __init__.py
│   │   └── models.py                # Database models
│   │
│   ├── services/                    # Services
│   │   ├── __init__.py
│   │   └── llm_service.py           # LLM integration
│   │
│   ├── tools/                       # Agent Tools
│   │   ├── __init__.py
│   │   ├── base.py                  # Base tool interface
│   │   ├── news_fetch.py            # News fetching
│   │   └── web_scrape.py            # Web scraping
│   │
│   ├── workers/                     # Background Tasks
│   │   ├── __init__.py
│   │   └── celery_app.py            # Celery configuration
│   │
│   └── jobs/                        # Scheduled Jobs
│       ├── __init__.py
│       └── news_automation.py       # Automated news fetching
│
├── tests/                           # Test Suite
│   ├── __init__.py
│   └── test_orchestrator.py         # Agent tests
│
├── scripts/                         # Utility Scripts
│   ├── deploy.sh                    # Deployment script
│   └── init_system.py               # System initialization
│
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── render.yaml                      # Render deployment config
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── pytest.ini                       # Test configuration
├── start.sh                         # Quick start script
├── README.md                        # Main documentation
├── DEPLOYMENT_GUIDE.md              # Deployment instructions
└── PROJECT_OVERVIEW.md              # This file
```

---

## 🔌 API Endpoints

### Agent Operations
```
POST   /api/v1/agent/execute        # Execute agent task
```

### Projects
```
POST   /api/v1/projects              # Create project
GET    /api/v1/projects              # List projects
GET    /api/v1/projects/{id}         # Get project
```

### Articles
```
POST   /api/v1/articles              # Create article
GET    /api/v1/articles              # List articles
GET    /api/v1/articles/{id}         # Get article
```

### Tasks
```
GET    /api/v1/tasks                 # List tasks
GET    /api/v1/tasks/{id}            # Get task
```

### News
```
POST   /api/v1/news/fetch            # Fetch news
```

### Content
```
POST   /api/v1/content/generate      # Generate content
```

### System
```
GET    /                             # Root endpoint
GET    /health                       # Health check
GET    /metrics                      # Prometheus metrics
GET    /docs                         # API documentation
```

---

## 🗄️ Database Schema

### Projects Table
```sql
- id (PK)
- name
- domain
- description
- status
- created_at
- updated_at
```

### Articles Table
```sql
- id (PK)
- project_id (FK)
- title
- content
- summary
- url
- source
- category
- published
- published_at
- metadata (JSON)
- created_at
- updated_at
```

### Tasks Table
```sql
- id (PK)
- project_id (FK)
- task_type
- description
- status
- agent_name
- input_data (JSON)
- result_data (JSON)
- error_message
- started_at
- completed_at
- created_at
```

### SEO Data Table
```sql
- id (PK)
- project_id (FK)
- url
- keyword
- ranking
- traffic
- impressions
- clicks
- ctr
- date
- metadata (JSON)
```

### Domains Table
```sql
- id (PK)
- name
- registrar
- expiration_date
- status
- price_paid
- current_value
- notes
- created_at
- updated_at
```

---

## 🔧 Configuration

### Required Environment Variables
```bash
# AI Models (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Security
SECRET_KEY=<generate-with-openssl>

# Database (auto-configured on Render)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

### Optional but Recommended
```bash
NEWS_API_KEY=...              # For enhanced news fetching
DEFAULT_MODEL=gpt-4           # Preferred LLM model
NEWS_FETCH_INTERVAL=30        # Minutes between fetches
CORS_ORIGINS=https://...      # Frontend origins
```

### Optional Social Media
```bash
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
FACEBOOK_ACCESS_TOKEN=...
```

---

## 🚀 Getting Started

### Local Development
```bash
# 1. Clone repository
git clone <repo-url>
cd manus-agent

# 2. Run quick start
chmod +x start.sh
./start.sh

# 3. Start services
# Terminal 1: Redis
redis-server

# Terminal 2: API
uvicorn app.main:app --reload

# Terminal 3: Worker
celery -A app.workers.celery_app worker --loglevel=info

# 4. Access
open http://localhost:8000/docs
```

### Production Deployment
```bash
# 1. Push to GitHub
git remote add origin <github-url>
git push -u origin main

# 2. Deploy to Render
# Follow DEPLOYMENT_GUIDE.md

# 3. Configure environment variables
# In Render dashboard

# 4. Verify deployment
curl https://your-app.onrender.com/health
```

---

## 📊 Monitoring & Observability

### Logging
- Structured logging with timestamps
- Log levels: INFO, WARNING, ERROR
- Centralized in Render dashboard

### Metrics
- Prometheus metrics endpoint: `/metrics`
- Request counts, latencies, errors
- Custom agent metrics

### LLM Monitoring (Optional)
- LangFuse integration for LLM observability
- Track token usage, costs, latencies
- Conversation tracing

### Health Checks
- API health: `/health`
- Database connectivity
- LLM service status

---

## 🔐 Security Features

1. **API Key Management**: Environment variables
2. **CORS Protection**: Configurable origins
3. **Input Validation**: Pydantic models
4. **Rate Limiting**: 60 requests/minute default
5. **SQL Injection Protection**: SQLAlchemy ORM
6. **JWT Authentication**: Ready for implementation

---

## 📈 Scaling Considerations

### Horizontal Scaling
- Add more web service instances
- Scale Celery workers independently
- Use load balancer

### Vertical Scaling
- Upgrade Render plans
- Increase database resources
- Add Redis memory

### Performance Optimization
- Database indexing
- Redis caching (TTL: 1 hour)
- Connection pooling
- Async operations

---

## 🧪 Testing

### Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=app

# Specific test
pytest tests/test_orchestrator.py

# Mark-based
pytest -m unit
pytest -m integration
```

### Test Coverage
- Unit tests for agents
- Integration tests for API
- Tool tests
- Database tests

---

## 🔄 CI/CD

### Automatic Deployment
- Push to `main` branch
- Render auto-detects changes
- Builds and deploys
- Zero-downtime deployment

### Build Process
1. Install dependencies
2. Install Playwright browsers
3. Run tests (optional)
4. Deploy services

---

## 💡 Use Cases

### 1. Breaking News Site (breakings.news)
```python
# Automated workflow:
1. Cron job fetches news every 30 minutes
2. Articles processed by LLM
3. SEO optimization applied
4. Content ready for publishing
5. Social media posts generated
```

### 2. Content Marketing
```python
# Generate blog post:
POST /api/v1/content/generate
{
  "topic": "Future of AI",
  "keywords": ["AI", "machine learning"],
  "content_type": "article"
}
```

### 3. SEO Optimization
```python
# Optimize existing content:
POST /api/v1/agent/execute
{
  "task": "Optimize my article for SEO",
  "context": {
    "content": "...",
    "keywords": [...]
  }
}
```

### 4. Research Assistant
```python
# Research and summarize:
POST /api/v1/agent/execute
{
  "task": "Research latest trends in quantum computing"
}
```

---

## 🛠️ Customization

### Add New Agent
1. Create agent class in `app/agents/`
2. Inherit from base agent
3. Implement execute method
4. Register in orchestrator

### Add New Tool
1. Create tool class in `app/tools/`
2. Inherit from `AgentTool`
3. Implement required methods
4. Use in agents

### Add API Endpoint
1. Add route in `app/api/routes.py`
2. Define request/response models
3. Implement logic
4. Test in `/docs`

---

## 📚 Documentation Links

- **API Docs**: `/docs` (Swagger UI)
- **README**: Main project documentation
- **Deployment Guide**: Step-by-step deployment
- **This File**: Architecture overview

---

## 🎯 Roadmap

### Phase 1: Foundation (✅ Complete)
- [x] Multi-agent architecture
- [x] News automation
- [x] Content generation
- [x] SEO optimization
- [x] Deployment configuration

### Phase 2: Enhancement (Next)
- [ ] Social media auto-publishing
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] A/B testing for content
- [ ] Multi-language support

### Phase 3: Advanced (Future)
- [ ] GraphQL API
- [ ] WebSocket real-time updates
- [ ] Chrome extension
- [ ] Mobile app
- [ ] Advanced analytics with ML

---

## 💰 Cost Analysis

### Render Hosting (Monthly)
- Web Service: $7
- Worker Service: $7
- PostgreSQL: $7
- Redis: $7
**Total: $28/month**

### API Costs (Variable)
- OpenAI GPT-4: ~$0.03/1K tokens
- Anthropic Claude: ~$0.015/1K tokens
- NewsAPI: Free (100 req/day) or $49/month (unlimited)

### Estimated Monthly (Light Usage)
- Hosting: $28
- OpenAI: ~$20-50
- NewsAPI: $0 (free tier)
**Total: ~$50-80/month**

---

## 🆘 Support

### Getting Help
1. Check README and DEPLOYMENT_GUIDE
2. Review API documentation
3. Check logs in Render dashboard
4. Open GitHub issue

### Common Issues
- **Build fails**: Check Python version (3.11+)
- **Database errors**: Verify DATABASE_URL
- **API errors**: Check API keys
- **News fetch fails**: Verify NewsAPI key

---

## 📝 Notes

- System uses OpenAI GPT-4 by default (can switch to Claude)
- News fetching runs every 30 minutes automatically
- All LLM responses are logged for debugging
- Database includes full audit trail
- Ready for production use

---

**Created**: November 2024  
**Version**: 1.0.0  
**Status**: Production Ready ✅
