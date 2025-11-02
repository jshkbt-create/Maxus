# 🚀 Complete Deployment Guide for Manus Agent System

This guide will walk you through deploying the Manus Agent System to Render.com from scratch.

## 📋 Prerequisites

Before you begin, ensure you have:

- [ ] GitHub account
- [ ] Render.com account (sign up at https://render.com)
- [ ] OpenAI API key OR Anthropic API key
- [ ] NewsAPI key (optional, get free at https://newsapi.org)
- [ ] Git installed on your machine

## 🎯 Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository

```bash
cd manus-agent
git init
git add .
git commit -m "Initial commit: Manus Agent System"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `manus-agent`
3. Visibility: Private (recommended) or Public
4. Do NOT initialize with README (we already have one)
5. Click "Create repository"

### 1.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/manus-agent.git
git branch -M main
git push -u origin main
```

## 🔑 Step 2: Get Your API Keys

### 2.1 OpenAI API Key (Recommended)

1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Name it: "Manus Agent"
5. Copy and save the key (starts with `sk-`)

### 2.2 Anthropic API Key (Alternative)

1. Go to https://console.anthropic.com
2. Sign in or create account
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy and save the key (starts with `sk-ant-`)

### 2.3 NewsAPI Key (Optional but Recommended)

1. Go to https://newsapi.org
2. Click "Get API Key"
3. Sign up (free tier: 100 requests/day)
4. Copy your API key

## 🌐 Step 3: Deploy to Render

### 3.1 Connect GitHub to Render

1. Log in to https://dashboard.render.com
2. Click "New +" in top right
3. Select "Blueprint"
4. Click "Connect GitHub"
5. Authorize Render to access your GitHub

### 3.2 Select Repository

1. Find and select `manus-agent` repository
2. Click "Connect"
3. Render will automatically detect `render.yaml`
4. Review the services that will be created:
   - `manus-agent-api` (Web Service)
   - `manus-worker` (Worker Service)
   - `news-automation` (Cron Job)
   - `manus-db` (PostgreSQL Database)
   - `manus-redis` (Redis Database)

### 3.3 Configure Environment Variables

Click on each service and add environment variables:

#### For `manus-agent-api` (Web Service):

**Required Variables:**
```
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here

SECRET_KEY=<click "Generate" button>
```

**Optional but Recommended:**
```
NEWS_API_KEY=your-newsapi-key
DEBUG=false
ENVIRONMENT=production
```

**Optional Social Media (add later if needed):**
```
TWITTER_API_KEY=your-twitter-key
TWITTER_API_SECRET=your-twitter-secret
FACEBOOK_ACCESS_TOKEN=your-facebook-token
```

### 3.4 Deploy

1. Review all configurations
2. Click "Apply" at the bottom
3. Render will now:
   - Create database instances
   - Build your application
   - Install dependencies
   - Deploy services

**First deployment takes 5-10 minutes**

## ✅ Step 4: Verify Deployment

### 4.1 Check Build Logs

1. Go to your `manus-agent-api` service
2. Click "Logs" tab
3. Watch for:
   ```
   🚀 Starting Manus Agent System...
   ✅ Database initialized
   ✅ LLM Service initialized
   ```

### 4.2 Test Health Endpoint

Once deployment is complete, you'll see a URL like:
```
https://manus-agent-api.onrender.com
```

Test it:
```bash
curl https://your-app.onrender.com/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "llm_service": "ready"
}
```

### 4.3 Access API Documentation

Visit: `https://your-app.onrender.com/docs`

You should see the interactive API documentation (Swagger UI).

## 🔧 Step 5: Initialize Your System

### 5.1 Create First Project

Using the API docs (`/docs`), or with curl:

```bash
curl -X POST https://your-app.onrender.com/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Breaking News",
    "domain": "breakings.news",
    "description": "Automated news aggregation"
  }'
```

### 5.2 Trigger First News Fetch

```bash
curl -X POST https://your-app.onrender.com/api/v1/news/fetch?category=technology&limit=10
```

### 5.3 Verify Cron Job

1. Go to `news-automation` cron job in Render
2. Click "Trigger Run" to test
3. Check logs to ensure it runs successfully
4. It will now run automatically every 30 minutes

## 🎨 Step 6: Test Agent Functionality

### 6.1 Test Orchestrator

```bash
curl -X POST https://your-app.onrender.com/api/v1/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Fetch latest AI news and summarize",
    "context": {}
  }'
```

### 6.2 Test Content Generation

```bash
curl -X POST https://your-app.onrender.com/api/v1/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of AI",
    "content_type": "article",
    "keywords": ["AI", "technology", "future"]
  }'
```

## 📊 Step 7: Monitoring & Maintenance

### 7.1 View Logs

- **Real-time logs**: Render Dashboard → Your Service → Logs
- **Download logs**: Available in dashboard

### 7.2 Monitor Performance

- **Metrics**: Render Dashboard → Your Service → Metrics
- **Prometheus**: `https://your-app.onrender.com/metrics`

### 7.3 Check Database

```bash
# Connect to PostgreSQL (get connection string from Render)
psql <DATABASE_URL>

# Check tables
\dt

# View projects
SELECT * FROM projects;

# View articles
SELECT * FROM articles LIMIT 10;
```

### 7.4 Monitor Worker

Check Celery worker logs in Render dashboard:
```
manus-worker → Logs
```

## 🔄 Step 8: Updates & Maintenance

### 8.1 Deploy Updates

```bash
# Make changes to code
git add .
git commit -m "Update: description of changes"
git push origin main
```

Render will automatically:
- Detect the push
- Build new version
- Deploy with zero downtime

### 8.2 Manage Environment Variables

To update environment variables:
1. Render Dashboard → Your Service → Environment
2. Add/Edit variables
3. Click "Save Changes"
4. Service will automatically restart

### 8.3 Database Migrations

If you make database schema changes:

```bash
# On your local machine
alembic revision --autogenerate -m "Description"
git add alembic/versions/
git commit -m "Add migration"
git push

# Render will run: alembic upgrade head automatically
```

## 🐛 Troubleshooting

### Issue: Build Fails

**Solution:**
1. Check build logs in Render dashboard
2. Verify `requirements.txt` is correct
3. Ensure Python version matches (3.11+)

### Issue: API Returns 500 Error

**Solution:**
1. Check application logs
2. Verify environment variables are set
3. Check database connection
4. Ensure API keys are valid

### Issue: Database Connection Error

**Solution:**
1. Verify `DATABASE_URL` is automatically set
2. Check database service is running
3. Restart web service

### Issue: News Fetch Not Working

**Solution:**
1. Check `NEWS_API_KEY` is set
2. Verify API key is valid at newsapi.org
3. Check cron job logs
4. Ensure rate limits aren't exceeded

### Issue: LLM Errors

**Solution:**
1. Verify `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is set
2. Check API key has sufficient credits
3. Test key independently
4. Check rate limits

## 💰 Cost Estimation

### Render Costs (as of 2024):

**Starter Plan (Recommended for testing):**
- Web Service: $7/month
- Worker Service: $7/month
- PostgreSQL: $7/month
- Redis: $7/month
- **Total: ~$28/month**

**Free Tier Option:**
- Limited to 750 hours/month
- Services spin down after inactivity
- Good for testing, not production

### API Costs:

- **OpenAI GPT-4**: ~$0.03 per 1K tokens
- **Anthropic Claude**: ~$0.015 per 1K tokens
- **NewsAPI Free**: 100 requests/day (sufficient for testing)

## 🎓 Next Steps

Now that you're deployed:

1. **Connect a Domain**: 
   - Render Dashboard → Settings → Custom Domain
   - Add `breakings.news` or your domain

2. **Set Up SSL**: 
   - Automatic with Render (Let's Encrypt)

3. **Build Frontend**:
   - Create React/Vue app
   - Connect to API
   - Deploy separately

4. **Add More Features**:
   - Social media publishing
   - Email notifications
   - Analytics dashboard

5. **Scale Up**:
   - Upgrade Render plans
   - Add more workers
   - Optimize database queries

## 📚 Additional Resources

- **Render Documentation**: https://render.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph
- **API Reference**: `https://your-app.onrender.com/docs`

## 🆘 Getting Help

If you encounter issues:

1. Check the logs first
2. Review this guide
3. Check GitHub Issues
4. Contact support

---

**Congratulations! Your Manus Agent System is now live! 🎉**
