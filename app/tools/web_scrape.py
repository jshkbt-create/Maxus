"""
Web Scraping Tool - Extract and analyze content from websites
"""
from typing import Dict, Any, Optional
import logging
import httpx
from datetime import datetime

from app.tools.base import BaseTool, ToolResult

logger = logging.getLogger(__name__)


class WebScrapeTool(BaseTool):
    """Tool for scraping and extracting content from websites"""

    @property
    def name(self) -> str:
        """Tool name"""
        return "WebScrapeTool"

    @property
    def description(self) -> str:
        """Tool description"""
        return "Scrapes content from websites and extracts text"

    async def execute(self, url: str, **kwargs) -> ToolResult:
        """
        Scrape a website and extract content
        
        Args:
            url: The URL to scrape
            
        Returns:
            ToolResult with scraped content
        """
        try:
            if not url or not isinstance(url, str):
                return ToolResult(success=False, error="Invalid URL provided")

            # Validate URL format
            if not (url.startswith("http://") or url.startswith("https://")):
                url = f"https://{url}"

            content = await self._scrape_content(url)
            
            return ToolResult(
                success=True,
                data={
                    "url": url,
                    "content": content.get("text", ""),
                    "title": content.get("title", ""),
                    "scraped_at": datetime.utcnow().isoformat(),
                    "char_count": len(content.get("text", "")),
                },
            )
        except Exception as e:
            logger.error(f"Web scrape error for {url}: {e}")
            return ToolResult(success=False, error=str(e))

    async def _scrape_content(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from a URL
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary with title and text content
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                    follow_redirects=True,
                )
                response.raise_for_status()
                
                html_content = response.text
                
                # Simple HTML to text extraction
                # For production, consider using BeautifulSoup or similar
                text_content = self._extract_text_from_html(html_content)
                title = self._extract_title_from_html(html_content)
                
                return {
                    "title": title or "Untitled",
                    "text": text_content,
                }
        except httpx.HTTPError as e:
            logger.error(f"HTTP error scraping {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            raise

    @staticmethod
    def _extract_title_from_html(html: str) -> Optional[str]:
        """Extract title from HTML"""
        try:
            # Simple regex-based extraction
            import re
            title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
            if title_match:
                return title_match.group(1).strip()
            
            # Try og:title
            og_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', html, re.IGNORECASE)
            if og_match:
                return og_match.group(1).strip()
        except Exception as e:
            logger.warning(f"Error extracting title: {e}")
        
        return None

    @staticmethod
    def _extract_text_from_html(html: str) -> str:
        """Extract plain text from HTML"""
        try:
            import re
            
            # Remove script and style elements
            clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
            clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
            
            # Remove HTML tags
            clean = re.sub(r'<[^>]+>', ' ', clean)
            
            # Remove multiple spaces
            clean = re.sub(r'\s+', ' ', clean)
            
            # Decode HTML entities
            import html as html_module
            clean = html_module.unescape(clean)
            
            return clean.strip()
        except Exception as e:
            logger.warning(f"Error extracting text: {e}")
            return html
