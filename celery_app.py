"""
Celery Configuration for Background Tasks
"""
from celery import Celery
from app.config import settings

# Initialize Celery app
celery_app = Celery(
    "manus_agent",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

@celery_app.task(name="process_news_article")
def process_news_article(article_id: int):
    """Process a single news article"""
    from app.db.database import SessionLocal
    from app.models.models import Article
    from app.services.llm_service import LLMService
    import asyncio
    
    db = SessionLocal()
    
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        
        if not article:
            return {"error": "Article not found"}
        
        # Process with LLM
        llm_service = LLMService()
        
        # Generate summary
        summary = asyncio.run(
            llm_service.summarize_text(article.content, max_length=150)
        )
        
        # Extract keywords
        keywords = asyncio.run(
            llm_service.extract_keywords(article.content, count=5)
        )
        
        # Update article
        article.summary = summary
        article.metadata = article.metadata or {}
        article.metadata["keywords"] = keywords
        
        db.commit()
        
        return {
            "success": True,
            "article_id": article_id,
            "summary": summary,
            "keywords": keywords
        }
    
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
    finally:
        db.close()

@celery_app.task(name="generate_social_posts")
def generate_social_posts(article_id: int):
    """Generate social media posts for an article"""
    from app.db.database import SessionLocal
    from app.models.models import Article
    from app.services.llm_service import LLMService
    from app.agents.content_agent import ContentAgent
    import asyncio
    
    db = SessionLocal()
    
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        
        if not article:
            return {"error": "Article not found"}
        
        llm_service = LLMService()
        content_agent = ContentAgent(llm_service)
        
        # Generate posts for different platforms
        platforms = ["twitter", "facebook", "linkedin"]
        posts = {}
        
        for platform in platforms:
            result = asyncio.run(
                content_agent.generate_social_content(
                    task=f"Create {platform} post",
                    context={
                        "platform": platform,
                        "topic": article.title,
                        "tone": "engaging"
                    }
                )
            )
            
            if result.get("success"):
                posts[platform] = result.get("content")
        
        # Save to article metadata
        article.metadata = article.metadata or {}
        article.metadata["social_posts"] = posts
        
        db.commit()
        
        return {
            "success": True,
            "article_id": article_id,
            "posts": posts
        }
    
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
    finally:
        db.close()

@celery_app.task(name="optimize_article_seo")
def optimize_article_seo(article_id: int):
    """Optimize article for SEO"""
    from app.db.database import SessionLocal
    from app.models.models import Article
    from app.services.llm_service import LLMService
    from app.agents.seo_agent import SEOAgent
    import asyncio
    
    db = SessionLocal()
    
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        
        if not article:
            return {"error": "Article not found"}
        
        llm_service = LLMService()
        seo_agent = SEOAgent(llm_service)
        
        # Get keywords from metadata
        keywords = article.metadata.get("keywords", []) if article.metadata else []
        
        # Optimize content
        result = asyncio.run(
            seo_agent.optimize_content(
                task="Optimize article for SEO",
                context={
                    "content": article.content,
                    "keywords": keywords
                }
            )
        )
        
        # Generate meta tags
        meta_tags = asyncio.run(
            seo_agent.generate_meta_tags(
                title=article.title,
                content=article.content,
                keywords=keywords
            )
        )
        
        # Update article
        article.metadata = article.metadata or {}
        article.metadata["seo"] = {
            "optimization": result.get("optimization"),
            "meta_tags": meta_tags
        }
        
        db.commit()
        
        return {
            "success": True,
            "article_id": article_id,
            "meta_tags": meta_tags
        }
    
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
    finally:
        db.close()
