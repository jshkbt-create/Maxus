"""
Celery Configuration for Background Tasks
"""
from celery import Celery
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create Celery app
celery_app = Celery(
    "manus_agent",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
)


@celery_app.task(bind=True)
def fetch_news_task(self, category: str = "technology", limit: int = 10):
    """Background task for fetching news"""
    try:
        from app.agents.news_agent import NewsAgent
        from app.services.llm_service import LLMService
        
        llm_service = LLMService()
        news_agent = NewsAgent(llm_service)
        
        import asyncio
        result = asyncio.run(news_agent.fetch_news(category=category, limit=limit))
        return result
    except Exception as e:
        logger.error(f"News fetch task error: {e}")
        raise


@celery_app.task(bind=True)
def generate_content_task(self, topic: str, content_type: str = "article"):
    """Background task for content generation"""
    try:
        from app.agents.content_agent import ContentAgent
        from app.services.llm_service import LLMService
        
        llm_service = LLMService()
        content_agent = ContentAgent(llm_service)
        
        import asyncio
        context = {"topic": topic}
        result = asyncio.run(content_agent.execute(
            task=f"Generate {content_type} about {topic}",
            context=context
        ))
        return result
    except Exception as e:
        logger.error(f"Content generation task error: {e}")
        raise


@celery_app.task(bind=True)
def optimize_seo_task(self, content: str, keywords: list):
    """Background task for SEO optimization"""
    try:
        from app.agents.seo_agent import SEOAgent
        from app.services.llm_service import LLMService
        
        llm_service = LLMService()
        seo_agent = SEOAgent(llm_service)
        
        import asyncio
        context = {"content": content, "keywords": keywords}
        result = asyncio.run(seo_agent.execute(
            task="Optimize content for SEO",
            context=context
        ))
        return result
    except Exception as e:
        logger.error(f"SEO optimization task error: {e}")
        raise
