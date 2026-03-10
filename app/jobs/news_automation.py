"""
News Automation Job - Runs every 30 minutes to fetch latest news
"""
import asyncio
import logging
from datetime import datetime

from app.agents.news_agent import NewsAgent
from app.services.llm_service import LLMService
from app.db.database import SessionLocal
from app.models.models import Article

logger = logging.getLogger(__name__)


async def fetch_and_store_news():
    """Fetch news and store in database"""
    try:
        logger.info("Starting news automation job")
        
        llm_service = LLMService()
        news_agent = NewsAgent(llm_service)
        
        # Fetch news from multiple categories
        categories = ["technology", "business", "science"]
        
        db = SessionLocal()
        
        for category in categories:
            try:
                logger.info(f"Fetching news for category: {category}")
                result = await news_agent.fetch_news(category=category, limit=10)
                
                if result.get("success") and result.get("articles"):
                    for article_data in result["articles"][:5]:  # Store top 5 per category
                        # Check if article already exists
                        existing = db.query(Article).filter(
                            Article.title == article_data.get("title")
                        ).first()
                        
                        if not existing:
                            article = Article(
                                title=article_data.get("title", "")[:500],
                                content=article_data.get("description", "")[:5000],
                                category=category,
                                source_url=article_data.get("url", ""),
                                status="published",
                            )
                            db.add(article)
                        
                        db.commit()
                
            except Exception as e:
                logger.error(f"Error fetching news for {category}: {e}")
                db.rollback()
        
        db.close()
        logger.info("News automation job completed successfully")
        return {"status": "success", "completed_at": datetime.utcnow().isoformat()}
        
    except Exception as e:
        logger.error(f"News automation job error: {e}")
        return {"status": "error", "error": str(e)}


def run_news_automation():
    """Run news automation synchronously"""
    return asyncio.run(fetch_and_store_news())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    result = run_news_automation()
    print(result)
