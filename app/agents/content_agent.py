"""
Content Agent - Fixed version with proper imports and error handling
"""
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class ContentAgent:
    """Agent specialized in content creation and management"""

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        logger.info("ContentAgent initialized")

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict:
        """Execute content-related task"""
        logger.info(f"ContentAgent executing: {task}")
        try:
            task_lower = task.lower()
            if "article" in task_lower or "write" in task_lower:
                return await self.generate_article(task, context)
            elif "social" in task_lower:
                return await self.generate_social_content(task, context)
            elif "rewrite" in task_lower:
                return await self.rewrite_content(task, context)
            else:
                return await self.generate_content(task, context)
        except Exception as e:
            logger.error(f"ContentAgent error: {e}")
            return {"error": str(e), "success": False}

    async def generate_article(self, task: str, context: Dict[str, Any]) -> Dict:
        """Generate a full article"""
        topic = context.get("topic", task)
        keywords = context.get("keywords", [])
        style = context.get("style", "news")
        length = context.get("length", 800)

        article_data = await self.llm_service.generate_article(
            topic=topic,
            keywords=keywords,
            style=style,
            length=length,
        )
        return {
            "success": True,
            "content_type": "article",
            "data": article_data,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "word_count": len(article_data.get("content", "").split()),
                "keywords": keywords,
            },
        }

    async def generate_social_content(self, task: str, context: Dict[str, Any]) -> Dict:
        """Generate social media content"""
        platform = context.get("platform", "twitter")
        topic = context.get("topic", task)
        tone = context.get("tone", "professional")

        system_prompt = f"""You are a social media content expert.
Create engaging {platform} content with a {tone} tone.
For Twitter: Keep under 280 characters.
For Facebook: 1-2 paragraphs, engaging and shareable.
For LinkedIn: Professional, 2-3 paragraphs."""

        messages = [{"role": "user", "content": f"Create {platform} post about: {topic}"}]
        content = await self.llm_service.chat(messages=messages, system_prompt=system_prompt)

        return {
            "success": True,
            "content_type": "social",
            "platform": platform,
            "content": content,
            "metadata": {
                "character_count": len(content),
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    async def rewrite_content(self, task: str, context: Dict[str, Any]) -> Dict:
        """Rewrite existing content"""
        original_content = context.get("content", "")
        instructions = context.get("instructions", task)

        system_prompt = """You are a professional content editor.
Rewrite the content according to the instructions while maintaining the core message."""

        messages = [{
            "role": "user",
            "content": f"Instructions: {instructions}\n\nOriginal content:\n{original_content}",
        }]
        rewritten = await self.llm_service.chat(messages=messages, system_prompt=system_prompt)

        return {
            "success": True,
            "content_type": "rewritten",
            "original": original_content,
            "rewritten": rewritten,
            "metadata": {"generated_at": datetime.utcnow().isoformat()},
        }

    async def generate_content(self, task: str, context: Dict[str, Any]) -> Dict:
        """Generate general content"""
        system_prompt = """You are a professional content creator.
Generate high-quality, engaging content based on the request."""
        messages = [{"role": "user", "content": task}]
        content = await self.llm_service.chat(messages=messages, system_prompt=system_prompt)

        return {
            "success": True,
            "content_type": "general",
            "content": content,
            "metadata": {"generated_at": datetime.utcnow().isoformat()},
        }
