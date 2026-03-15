# 🚀 DEPLOY NOW - Quick Deployment Guide

**Status:** ✅ System Ready for Deployment
**Time to Deploy:** 5-10 minutes
**All Issues:** ✅ Fixed

---

## 📋 Pre-Deployment Checklist (2 minutes)

```bash
# 1. Verify all files are present
python verify.py

# Should output:
# ✅ Installation verification PASSED
```

**Expected Output:** All files present ✅

---

## 🔑 Required API Keys

Choose ONE of these:

### Option A: OpenAI (Recommended)
1. Get key: https://platform.openai.com/api-keys
2. Create a new API key
3. Add to .env: `OPENAI_API_KEY=sk-...`

### Option B: Anthropic
1. Get key: https://console.anthropic.com
2. Create a new API key  
3. Add to .env: `ANTHROPIC_API_KEY=sk-ant-...`

### Option C: Both (Best Option)
Add both keys - system will use fallback if one fails

---

## 🌐 Optional: NewsAPI Key

For real news data:
1. Get free key: https://newsapi.org
2. Add to .env: `NEWS_API_KEY=...`

(If not set, system uses mock news data)

---

## 📝 Step 1: Configure Environment

### Edit `.env` file

```bash
# Open the .env file in your editor
# Set your API keys:

LLM_PROVIDER=anthropic  # or openai
OPENAI_API_KEY=sk-...   # If using OpenAI
ANTHROPIC_API_KEY=sk-ant-...  # If using Anthropic
NEWS_API_KEY=...        # Optional, for real news
```

---

## 🔧 Step 2: Deploy to Render.com

### Method 1: One-Click Deploy (Easiest)

1. Push code to GitHub:
```bash
git add .
git commit -m "Production ready - all issues fixed"
git push origin main
```

2. Go to Render Dashboard:
   - URL: https://dashboard.render.com
   - Click "New +"
   - Select "Blueprint"
   - Connect your GitHub repo
   - Click "Apply"

3. Wait 5-10 minutes for deployment

4. Your API is live! 🎉

### Method 2: Manual Deploy (If needed)

If you prefer manual setup:

1. Create web service on Render:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. Add environment variables in Render dashboard

3. Create PostgreSQL database (free tier available)

4. Create Redis database (free tier available)

---

## ✅ Step 3: Verify Deployment

Once deployed, check:

### 1. Health Check
```bash
curl https://your-app.onrender.com/health
# Should return: {"status": "healthy", "service": "manus-agent"}
```

### 2. Service Info
```bash
curl https://your-app.onrender.com/
# Should return service info
```

### 3. API Documentation
```
Visit: https://your-app.onrender.com/docs
```

### 4. Create a Project
```bash
curl -X POST https://your-app.onrender.com/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project", "domain": "example.com"}'
```

---

## 🧪 Test Your System

### Create a Test Project
```bash
curl -X POST https://your-app.onrender.com/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First Project",
    "domain": "myproject.com",
    "description": "Test project"
  }'
```

### Fetch News
```bash
curl -X POST "https://your-app.onrender.com/api/v1/news/fetch?category=technology&limit=5"
```

### Generate Content
```bash
curl -X POST "https://your-app.onrender.com/api/v1/content/generate?topic=AI&content_type=article"
```

### Run Agent Task
```bash
curl -X POST https://your-app.onrender.com/api/v1/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Fetch latest technology news",
    "context": {}
  }'
```

---

## 🔍 Monitor Your System

### In Render Dashboard
1. Go to your web service
2. Click "Logs" to see real-time logs
3. Check for any errors
4. Monitor CPU and memory usage

### Check Health Metrics
```bash
# API should be responding
curl https://your-app.onrender.com/health

# Should be instant response (< 100ms)
```

---

## 🆘 Troubleshooting

### "Service not found" error
- Wait 2-3 minutes after deployment
- Refresh page
- Check Render dashboard logs

### "Database connection error"
- Verify DATABASE_URL in environment variables
- Check if PostgreSQL service is running
- Wait 1-2 minutes for services to initialize

### "API key not found"
- Check environment variables in Render dashboard
- Ensure key is properly set (not just added to .env)
- Restart the service after changing vars

### "500 Internal Server Error"
- Check logs in Render dashboard
- Verify all dependencies installed
- Ensure API keys are valid

### "WebScrapeTool not found"
- Already created at `/app/tools/web_scrape.py` ✅
- If error persists, reinstall dependencies

---

## 📊 After Deployment

### Monitor Performance
- Check response times
- Monitor error rates
- Check database connections
- Monitor API usage

### Scale if Needed
- Upgrade Render plan from Free to Pro
- Add more database resources
- Configure auto-scaling

### Maintain Your System
- Check logs regularly
- Monitor resource usage
- Keep dependencies updated
- Test new features

---

## 🎯 Success Indicators

You're good to go when you see:

✅ Service running on Render
✅ `/health` endpoint returns healthy
✅ `/docs` shows API documentation
✅ Can create projects via API
✅ Can fetch news
✅ Can generate content
✅ No errors in logs

---

## 💡 Pro Tips

1. **Set up monitoring:**
   - Enable Render notifications
   - Monitor error rates
   - Track API usage

2. **Security:**
   - Use strong SECRET_KEY
   - Keep API keys private
   - Use HTTPS only (Render does this by default)
   - Enable rate limiting (optional)

3. **Optimization:**
   - Cache frequently accessed data
   - Use background jobs for heavy tasks
   - Monitor and optimize slow queries

4. **Backup:**
   - Enable PostgreSQL backups
   - Backup regularly
   - Test restore process

---

## 📚 Quick Documentation Links

- **Full Guide:** `/DEPLOYMENT_GUIDE.md`
- **Checklist:** `/DEPLOYMENT_CHECKLIST.md`
- **Audit Report:** `/AUDIT_REPORT.md`
- **Quick Reference:** `/QUICK_REFERENCE.md`
- **README:** `/README.md`

---

## ✨ You Did It! 🎉

Your Manus Agent System is now:
- ✅ Configured
- ✅ Deployed
- ✅ Running
- ✅ Monitored

**Celebrate! Your production AI system is live! 🚀**

---

## 📞 Next Steps

1. **Use the API:** Visit `/docs` endpoint
2. **Create projects:** Start organizing your content
3. **Fetch news:** Automate news gathering
4. **Generate content:** Use AI to create articles
5. **Monitor:** Watch logs and performance
6. **Scale:** Add more resources as needed

---

## 🆘 Need Help?

1. Check the logs in Render dashboard
2. Review `/AUDIT_REPORT.md` for detailed info
3. Run `python verify.py` locally to check structure
4. Read error messages carefully
5. Check API documentation at `/docs`

---

**Deployment Status:** ✅ READY
**All Issues:** ✅ FIXED
**System Status:** ✅ PRODUCTION READY

**Go build amazing things! 🚀**
