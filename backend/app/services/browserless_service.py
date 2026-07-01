"""
Browserless API Client
=======================
Async HTTP client for Browserless API using aiohttp
"""

import json
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

import aiohttp
from aiohttp import ClientTimeout, ClientError

from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class BrowserlessResult:
    """Result from Browserless API call"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    screenshot: Optional[str] = None
    pdf: Optional[bytes] = None
    execution_time_ms: Optional[float] = None


class BrowserlessClient:
    """
    Async client for Browserless Chrome API
    Supports scraping, screenshots, and PDF generation
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        timeout: int = 30
    ):
        self.api_key = api_key or settings.BROWSERLESS_API_KEY
        self.api_url = api_url or settings.BROWSERLESS_API_URL or "https://chrome.browserless.io"
        self.timeout = ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            headers = {
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            self._session = aiohttp.ClientSession(
                headers=headers,
                timeout=self.timeout
            )
        return self._session

    async def close(self) -> None:
        """Close the HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.info("Browserless session closed")

    async def scrape(
        self,
        url: str,
        selectors: Optional[List[str]] = None,
        wait_for_selector: Optional[str] = None,
        goto_options: Optional[Dict[str, Any]] = None,
        inject_js: Optional[str] = None
    ) -> BrowserlessResult:
        """
        Scrape content from a webpage
        
        Args:
            url: Target URL to scrape
            selectors: CSS selectors to extract (optional)
            wait_for_selector: Selector to wait for before scraping
            goto_options: Navigation options (waitUntil, timeout, etc.)
            inject_js: JavaScript to inject before scraping
        """
        start_time = datetime.now()
        
        payload = {
            "url": url,
            "elements": []
        }
        
        # Add selectors for extraction
        if selectors:
            for selector in selectors:
                payload["elements"].append({"selector": selector})
        
        # Configure navigation
        if wait_for_selector:
            payload["gotoOptions"] = {
                "waitUntil": "networkidle2",
                **(goto_options or {})
            }
            payload["waitForSelector"] = wait_for_selector
        
        # Inject custom JavaScript
        if inject_js:
            payload["injectJs"] = inject_js
        
        try:
            session = await self._get_session()
            
            async with session.post(
                f"{self.api_url}/scrape",
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    execution_time = (datetime.now() - start_time).total_seconds() * 1000
                    
                    return BrowserlessResult(
                        success=True,
                        data=data.get("data", {}),
                        screenshot=data.get("screenshot"),
                        execution_time_ms=execution_time
                    )
                else:
                    error_text = await response.text()
                    logger.error(f"Browserless scrape error: {response.status} - {error_text}")
                    return BrowserlessResult(
                        success=False,
                        error=f"HTTP {response.status}: {error_text}"
                    )
                    
        except ClientError as e:
            logger.error(f"Browserless connection error: {e}")
            return BrowserlessResult(
                success=False,
                error=f"Connection error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Browserless unexpected error: {e}")
            return BrowserlessResult(
                success=False,
                error=f"Unexpected error: {str(e)}"
            )

    async def screenshot(
        self,
        url: str,
        full_page: bool = False,
        viewport: Optional[Dict[str, int]] = None
    ) -> BrowserlessResult:
        """
        Take a screenshot of a webpage
        
        Args:
            url: Target URL
            full_page: Capture full page or just viewport
            viewport: Viewport dimensions {width, height}
        """
        payload = {
            "url": url,
            "options": {
                "fullPage": full_page,
                "type": "png"
            }
        }
        
        if viewport:
            payload["options"]["viewport"] = viewport
        
        try:
            session = await self._get_session()
            
            async with session.post(
                f"{self.api_url}/screenshot",
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return BrowserlessResult(
                        success=True,
                        screenshot=data.get("screenshot", data.get("data"))
                    )
                else:
                    error_text = await response.text()
                    return BrowserlessResult(
                        success=False,
                        error=f"HTTP {response.status}: {error_text}"
                    )
                    
        except ClientError as e:
            return BrowserlessResult(
                success=False,
                error=f"Connection error: {str(e)}"
            )

    async def pdf(
        self,
        url: str,
        options: Optional[Dict[str, Any]] = None
    ) -> BrowserlessResult:
        """
        Generate PDF from webpage
        
        Args:
            url: Target URL
            options: PDF generation options (format, landscape, margins, etc.)
        """
        payload = {
            "url": url,
            "options": options or {}
        }
        
        try:
            session = await self._get_session()
            
            async with session.post(
                f"{self.api_url}/pdf",
                json=payload
            ) as response:
                if response.status == 200:
                    pdf_bytes = await response.read()
                    return BrowserlessResult(
                        success=True,
                        pdf=pdf_bytes
                    )
                else:
                    error_text = await response.text()
                    return BrowserlessResult(
                        success=False,
                        error=f"HTTP {response.status}: {error_text}"
                    )
                    
        except ClientError as e:
            return BrowserlessResult(
                success=False,
                error=f"Connection error: {str(e)}"
            )

    async def evaluate(
        self,
        url: str,
        script: str,
        wait_for_selector: Optional[str] = None
    ) -> BrowserlessResult:
        """
        Execute JavaScript on a webpage and return results
        
        Args:
            url: Target URL
            script: JavaScript code to execute
            wait_for_selector: Optional selector to wait for before running script
        """
        payload = {
            "url": url,
            "context": {
                "function": script
            }
        }
        
        if wait_for_selector:
            payload["waitForSelector"] = wait_for_selector
        
        try:
            session = await self._get_session()
            
            async with session.post(
                f"{self.api_url}/function",
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return BrowserlessResult(
                        success=True,
                        data=data.get("data")
                    )
                else:
                    error_text = await response.text()
                    return BrowserlessResult(
                        success=False,
                        error=f"HTTP {response.status}: {error_text}"
                    )
                    
        except ClientError as e:
            return BrowserlessResult(
                success=False,
                error=f"Connection error: {str(e)}"
            )


# Singleton instance
browserless_client = BrowserlessClient()


# Convenience function
async def get_browserless() -> BrowserlessClient:
    """Get Browserless client instance"""
    return browserless_client
