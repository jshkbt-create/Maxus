"""
News Agent - Fetches, processes, and analyzes news
"""
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from app.services.llm_service import LLMService
from app.config import settings

logger = logging.getLogger(__name__)


class NewsAgent:
    """Agent for fetching and processing news"""

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.news_api_key = settings.NEWS_API_KEY
        logger.info("NewsAgent initialized")

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict:
        """Execute news-related task"""
        logger.info(f"NewsAgent executing: {task}")
        try:
            task_lower = task.lower()
            if "fetch" in task_lower or "get" in task_lower:
                category = context.get("category", "technology")
                keywords = context.get("keywords", "")
                limit = context.get("limit", 10)
                return await self.fetch_news(category=category, keywords=keywords, limit=limit)
            elif "analyze" in task_lower:
                articles = context.get("articles", [])
                return await self.analyze_news(articles)
            else:
                return await self.fetch_news()
        except Exception as e:
            logger.error(f"NewsAgent error: {e}")
            return {"error": str(e), "success": False}

    async def fetch_news(
        self,
        category: str = "technology",
        keywords: str = "",
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Fetch news articles from NewsAPI"""
        if not self.news_api_key:
            logger.warning("NEWS_API_KEY not set, returning mock data")
            return self._mock_news_data(category, limit)

        try:
            import httpx
            base_url = "https://newsapi.org/v2/top-headlines"
            params = {
                "category": category,
                "language": "en",
                "pageSize": limit,
                "apiKey": self.news_api_key,
            }
            if keywords:
                params["q"] = keywords

            async with httpx.AsyncClient() as client:
                response = await client.get(base_url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()

            articles = data.get("articles", [])
            return {
                "success": True,
                "category": category,
                "total_results": data.get("totalResults", 0),
                "articles": articles[:limit],
                "fetched_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"News fetch error: {e}")
            return {"error": str(e), "success": False}

    async def analyze_news(self, articles: List[Dict]) -> Dict[str, Any]:
        """Analyze a list of news articles"""
        if not articles:
            return {"error": "No articles to analyze", "success": False}

        summaries = []
        for article in articles[:5]:  # Limit to 5 to avoid token limits
            content = article.get("content") or article.get("description", "")
            if content:
                summary = await self.llm_service.summarize_text(content, max_length=100)
                summaries.append({
                    "title": article.get("title", ""),
                    "summary": summary,
                    "url": article.get("url", ""),
                })

        return {
            "success": True,
            "analyzed_count": len(summaries),
            "summaries": summaries,
            "analyzed_at": datetime.utcnow().isoformat(),
        }

    def _mock_news_data(self, category: str, limit: int) -> Dict[str, Any]:
        """Return mock news data when API key is not configured"""
        mock_articles = [
            {
                "title": f"Mock News Article {i+1} - {category.title()}",
                "description": f"This is a mock news article about {category}. Configure NEWS_API_KEY for real data.",
                "url": f"https://example.com/news/{i+1}",
                "publishedAt": datetime.utcnow().isoformat(),
                "source": {"name": "Mock Source"},
            }
            for i in range(min(limit, 3))
        ]
        return {
            "success": True,
            "category": category,
            "total_results": len(mock_articles),
            "articles": mock_articles,
            "fetched_at": datetime.utcnow().isoformat(),
            "note": "Mock data - configure NEWS_API_KEY for real news",
        }
