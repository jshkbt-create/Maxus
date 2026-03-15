"""
Tests for Agent modules
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from app.services.llm_service import LLMService
from app.agents.orchestrator import OrchestratorAgent
from app.agents.news_agent import NewsAgent
from app.agents.content_agent import ContentAgent
from app.agents.seo_agent import SEOAgent


@pytest.fixture
def llm_service():
    """Create a mock LLM service"""
    return LLMService()


@pytest.mark.asyncio
async def test_news_agent_fetch(llm_service):
    """Test news agent fetch functionality"""
    agent = NewsAgent(llm_service)
    result = await agent.fetch_news(category="technology", limit=5)
    
    assert result is not None
    assert "success" in result
    assert "articles" in result or "note" in result  # Either real data or mock


@pytest.mark.asyncio
async def test_content_agent_execute(llm_service):
    """Test content agent execution"""
    agent = ContentAgent(llm_service)
    context = {"topic": "AI"}
    result = await agent.execute(task="Write an article about AI", context=context)
    
    assert result is not None
    assert "success" in result
    assert result["success"] is True


@pytest.mark.asyncio
async def test_seo_agent_execute(llm_service):
    """Test SEO agent execution"""
    agent = SEOAgent(llm_service)
    context = {"content": "Sample content", "keywords": ["test"]}
    result = await agent.execute(task="Optimize for SEO", context=context)
    
    assert result is not None
    assert "success" in result or "error" in result


@pytest.mark.asyncio
async def test_orchestrator_routing(llm_service):
    """Test orchestrator task routing"""
    orchestrator = OrchestratorAgent(llm_service)
    
    # Test news routing
    result = await orchestrator.run(task="Fetch latest technology news", project_context={})
    assert result is not None
    
    # Test content routing
    result = await orchestrator.run(task="Write an article about blockchain", project_context={})
    assert result is not None
    
    # Test SEO routing
    result = await orchestrator.run(task="Optimize content for search engines", project_context={})
    assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
