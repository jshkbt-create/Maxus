# Manus Agent System 🤖

A sophisticated multi-agent system built with LangGraph for managing content automation, news aggregation, SEO optimization, and domain portfolio management. Designed specifically for **breakings.news** and your domain ecosystem.

## 🌟 Features

### Core Capabilities
- **🤖 Multi-Agent Architecture**: Orchestrator coordinates specialized agents (News, SEO, Content)
- **📰 Automated News Aggregation**: Fetch breaking news every 30 minutes from multiple sources
- **✍️ AI Content Generation**: Create articles, blog posts, and social media content
- **🔍 SEO Optimization**: Automated keyword research, meta tags, and content optimization
- **🌐 Web Scraping**: Extract content from any website (static and JavaScript-heavy)
- **📊 Task Management**: Track and monitor all agent tasks
- **🔄 Background Processing**: Celery workers for async tasks

### Specialized Agents
1. **Orchestrator Agent**: Main coordinator that analyzes tasks and delegates to specialists
2. **News Agent**: Fetches, processes, and analyzes breaking news
3. **SEO Agent**: Optimizes content for search engines
4. **Content Agent**: Generates articles, social posts, and rewrites content

## 📁 Project Structure

```
manus-agent/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration management
│   ├── agents/
│   │   ├── orchestrator.py    # Main orchestrator agent
│   │   ├── news_agent.py      # News fetching & processing
│   │   ├── seo_agent.py       # SEO optimization
│   │   └── content_agent.py   # Content generation
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── db/
│   │   └── database.py        # Database connection
│   ├── models/
│   │   └── models.py          # SQLAlchemy models
│   ├── services/
│   │   └── llm_service.py     # LLM integration (OpenAI/Anthropic)
│   ├── tools/
│   │   ├── base.py            # Base tool interface
│   │   ├── news_fetch.py      # News fetching tool
│   │   └── web_scrape.py      # Web scraping tool
│   ├── workers/
│   │   └── celery_app.py      # Celery background tasks
│   └── jobs/
│       └── news_automation.py # Scheduled news automation
├── tests/                      # Test files
├── scripts/                    # Utility scripts
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── render.yaml               # Render deployment config
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- OpenAI API Key or Anthropic API Key
- NewsAPI Key (optional, for enhanced news fetching)

### Local Development Setup

1. **Clone and Setup**
```bash
git clone <your-repo-url>
cd manus-agent
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. **Setup Database**
```bash
# Create PostgreSQL database
createdb manus_agent

# Run migrations (if using Alembic)
alembic upgrade head
```

6. **Start Services**

Terminal 1 - Main API:
```bash
uvicorn app.main:app --reload --port 8000
```

Terminal 2 - Celery Worker:
```bash
celery -A app.workers.celery_app worker --loglevel=info
```

Terminal 3 - Redis:
```bash
redis-server
```

7. **Access the API**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 🌐 Deployment to Render

### Option 1: Using Render Blueprint (Recommended)

1. **Prepare Your Repository**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy to Render**
- Go to [Render Dashboard](https://dashboard.render.com)
- Click "New +" → "Blueprint"
- Connect your GitHub repository
- Render will automatically detect `render.yaml`
- Click "Apply"

3. **Configure Environment Variables**

In Render dashboard, add these variables to your web service:

**Required:**
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
NEWS_API_KEY=...
SECRET_KEY=<generate-with-openssl-rand-hex-32>
```

**Optional:**
```
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
FACEBOOK_ACCESS_TOKEN=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
```

4. **Deploy**
- Render will automatically build and deploy
- First deployment: ~5-10 minutes
- Database and Redis are created automatically

### Option 2: Manual Deployment

1. **Create Services Manually**

**Web Service:**
- Name: manus-agent-api
- Environment: Python
- Build Command: `pip install -r requirements.txt && playwright install chromium`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Worker Service:**
- Name: manus-worker
- Environment: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `celery -A app.workers.celery_app worker --loglevel=info`

**Cron Job:**
- Name: news-automation
- Schedule: `*/30 * * * *` (every 30 minutes)
- Command: `python app/jobs/news_automation.py`

2. **Create Databases**
- PostgreSQL (Starter plan)
- Redis (Starter plan)

3. **Connect Services**
- Link DATABASE_URL from PostgreSQL
- Link REDIS_URL from Redis

## 📡 API Endpoints

### Agent Execution
```bash
POST /api/v1/agent/execute
{
  "task": "Fetch latest technology news",
  "project_id": 1,
  "context": {}
}
```

### News Operations
```bash
# Fetch news
POST /api/v1/news/fetch?category=technology&limit=10

# Response
{
  "articles": [...],
  "total": 10
}
```

### Content Generation
```bash
POST /api/v1/content/generate
{
  "topic": "AI in Healthcare",
  "content_type": "article",
  "keywords": ["AI", "healthcare", "machine learning"]
}
```

### Project Management
```bash
# Create project
POST /api/v1/projects
{
  "name": "Breaking News",
  "domain": "breakings.news",
  "description": "News aggregation site"
}

# List projects
GET /api/v1/projects

# Get project
GET /api/v1/projects/1
```

### Article Management
```bash
# Create article
POST /api/v1/articles
{
  "project_id": 1,
  "title": "Breaking: New AI Breakthrough",
  "content": "...",
  "category": "technology"
}

# List articles
GET /api/v1/articles?project_id=1

# Get article
GET /api/v1/articles/1
```

### Task Monitoring
```bash
# List tasks
GET /api/v1/tasks?status=completed

# Get task
GET /api/v1/tasks/1
```

## 🔧 Configuration

### Environment Variables

See `.env.example` for all configuration options. Key variables:

```bash
# AI Models
OPENAI_API_KEY=sk-...          # Required for GPT models
ANTHROPIC_API_KEY=sk-ant-...   # Required for Claude models
DEFAULT_MODEL=gpt-4             # Default LLM model

# Database
DATABASE_URL=postgresql://...   # Auto-configured on Render
REDIS_URL=redis://...          # Auto-configured on Render

# News
NEWS_API_KEY=...               # Get from newsapi.org
NEWS_FETCH_INTERVAL=30         # Minutes between auto-fetches

# Security
SECRET_KEY=...                 # Generate: openssl rand -hex 32

# CORS
CORS_ORIGINS=http://localhost:3000,https://breakings.news
```

## 🤖 Using the Agents

### Example: Fetch and Process News

```python
from app.services.llm_service import LLMService
from app.agents.orchestrator import OrchestratorAgent

# Initialize
llm_service = LLMService()
orchestrator = OrchestratorAgent(llm_service)

# Execute task
result = await orchestrator.run(
    task="Fetch latest AI news and create an article",
    project_context={"project_id": 1}
)

print(result)
```

### Example: Generate SEO-Optimized Content

```python
from app.agents.content_agent import ContentAgent
from app.agents.seo_agent import SEOAgent

# Generate content
content_agent = ContentAgent(llm_service)
article = await content_agent.generate_article(
    task="Write article about quantum computing",
    context={
        "keywords": ["quantum computing", "qubits", "superposition"],
        "length": 1000
    }
)

# Optimize for SEO
seo_agent = SEOAgent(llm_service)
optimized = await seo_agent.optimize_content(
    task="Optimize for SEO",
    context={
        "content": article["data"]["content"],
        "keywords": ["quantum computing"]
    }
)
```

## 📊 Monitoring

### Health Checks
```bash
# API health
curl https://your-app.onrender.com/health

# Prometheus metrics
curl https://your-app.onrender.com/metrics
```

### Logs
- **Render Dashboard**: View real-time logs
- **Application logs**: Structured JSON logging
- **LangFuse**: LLM observability (if configured)

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_agents.py::test_orchestrator
```

## 🔐 Security

- API keys stored in environment variables
- JWT-based authentication (configure in routes)
- Rate limiting enabled (60 req/min default)
- CORS configuration for frontend
- Input validation with Pydantic

## 📈 Scaling

### Horizontal Scaling
- Add more Render instances
- Configure load balancer
- Use Redis for session management

### Background Jobs
- Celery workers scale independently
- Add workers: `render scale manus-worker --replicas 3`

### Database
- Upgrade Render database plan
- Add read replicas
- Enable connection pooling

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Ensure you're in project root
export PYTHONPATH=$PWD
```

**2. Database Connection**
```bash
# Check DATABASE_URL is set
echo $DATABASE_URL
```

**3. Playwright Issues**
```bash
# Reinstall browsers
playwright install chromium
```

**4. Redis Connection**
```bash
# Verify Redis is running
redis-cli ping
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📝 License

[Your License Here]

## 🙋 Support

- **Issues**: GitHub Issues
- **Documentation**: `/docs` endpoint
- **Email**: your-email@example.com

## 🚀 Roadmap

- [ ] Add more specialized agents (Analytics, Social Media Publisher)
- [ ] Implement webhook system for real-time updates
- [ ] Add GraphQL API
- [ ] Create admin dashboard
- [ ] Implement A/B testing for content
- [ ] Add multi-language support
- [ ] Integrate more news sources
- [ ] Build Chrome extension for content management

---

**Built with ❤️ using LangGraph, FastAPI, and Anthropic Claude**
