"""Browser automation for web crawling"""

from typing import Any

from playwright.async_api import async_playwright, Browser, Page


class BrowserManager:
    """Manages browser instances for crawling"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser: Browser | None = None
    
    async def start(self) -> Browser:
        """Start browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        return self.browser
    
    async def new_page(self) -> Page:
        """Create new page"""
        if not self.browser:
            await self.start()
        return await self.browser.new_page()
    
    async def close(self) -> None:
        """Close browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def screenshot(self, url: str, path: str) -> None:
        """Take screenshot of page"""
        page = await self.new_page()
        await page.goto(url)
        await page.screenshot(path=path)
        await page.close()


async def get_browser(headless: bool = True) -> BrowserManager:
    """Get browser manager"""
    manager = BrowserManager(headless=headless)
    await manager.start()
    return manager
