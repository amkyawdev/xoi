"""
Controller Orchestrator
=======================
Central Controller that bridges Telegram Bot, Neon DB, and Browserless API
"""

import logging
import asyncio
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.connection import db_manager
from app.database.models import User, Conversation, Message, CacheEntry, UserState
from app.services.browserless_service import BrowserlessClient, browserless_client
from app.services.cache_service import cache_service, state_service
from app.middleware.error_handler import (
    error_handler,
    AgenticError,
    BrowserlessError,
    DatabaseError,
    ErrorSeverity
)

logger = logging.getLogger(__name__)


@dataclass
class TelegramUpdate:
    """Parsed Telegram update data"""
    update_id: int
    user_id: Optional[int] = None
    username: Optional[str] = None
    chat_id: Optional[int] = None
    message_text: Optional[str] = None
    command: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ControllerResponse:
    """Response from controller operation"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    should_reply: bool = True
    reply_markup: Optional[Any] = None
    notify_user: bool = True


class Controller:
    """
    Central Controller for Agentic Workflow
    =======================================
    
    Coordinates the following flow:
    1. Receive Telegram update
    2. Check Neon DB for existing data (Cache/State)
    3. If data missing or stale, trigger Browserless API
    4. Store processed result in Neon DB
    5. Return formatted response to Telegram Bot
    """
    
    def __init__(
        self,
        browserless: Optional[BrowserlessClient] = None,
        cache_ttl: int = 3600,
        state_ttl: int = 1800
    ):
        self.browserless = browserless or browserless_client
        self.cache_ttl = cache_ttl  # Default 1 hour
        self.state_ttl = state_ttl  # Default 30 minutes
        self.error_handler = error_handler
        
        # Operation timeouts
        self.browserless_timeout = 30
        self.db_timeout = 10
        
        logger.info("Controller initialized")

    async def process_update(self, update: TelegramUpdate) -> ControllerResponse:
        """
        Main entry point for processing Telegram updates
        
        Args:
            update: Parsed Telegram update
            
        Returns:
            ControllerResponse with reply message and data
        """
        logger.info(f"Processing update {update.update_id} from user {update.user_id}")
        
        try:
            # Step 1: Get or create user
            user = await self._get_or_create_user(update)
            if user is None:
                return ControllerResponse(
                    success=False,
                    message="⚠️ Failed to process user. Please try again."
                )
            
            # Step 2: Check user state (conversation context)
            user_state = await state_service.get_state(
                user_id=user.id,
                state_key="current_context"
            )
            
            # Step 3: Route based on command or message
            if update.command:
                return await self._handle_command(update, user, user_state)
            else:
                return await self._handle_message(update, user, user_state)
                
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            error_response = await self.error_handler.handle_error(
                e,
                context={
                    "update_id": update.update_id,
                    "user_id": update.user_id,
                    "operation": "process_update"
                },
                user_id=update.user_id
            )
            
            return ControllerResponse(
                success=False,
                message="⚠️ An error occurred while processing your request. Please try again."
            )

    async def _handle_command(
        self,
        update: TelegramUpdate,
        user: User,
        user_state: Optional[Dict]
    ) -> ControllerResponse:
        """Handle Telegram commands"""
        command = update.command.lower()
        
        # Command handlers
        handlers = {
            "/start": self._cmd_start,
            "/help": self._cmd_help,
            "/scrape": self._cmd_scrape,
            "/screenshot": self._cmd_screenshot,
            "/history": self._cmd_history,
            "/clear": self._cmd_clear,
            "/settings": self._cmd_settings,
        }
        
        handler = handlers.get(command)
        if handler:
            try:
                return await handler(update, user, user_state)
            except Exception as e:
                logger.error(f"Command handler error: {e}")
                return ControllerResponse(
                    success=False,
                    message=f"Error executing command: {str(e)}"
                )
        
        return ControllerResponse(
            success=False,
            message=f"Unknown command: {command}. Type /help for available commands."
        )

    async def _handle_message(
        self,
        update: TelegramUpdate,
        user: User,
        user_state: Optional[Dict]
    ) -> ControllerResponse:
        """Handle regular messages"""
        message_text = update.message_text or ""
        
        # Check cache first
        cache_key = cache_service.generate_key(
            "message",
            user.id,
            hashlib.md5(message_text.encode()).hexdigest()
        )
        
        cached_result = await cache_service.get(user.id, cache_key)
        if cached_result:
            logger.debug(f"Cache hit for message: {cache_key}")
            return ControllerResponse(
                success=True,
                message=cached_result.get("message", "Cached response"),
                data=cached_result
            )
        
        # URL detection for scraping
        if self._is_url(message_text):
            return await self._scrape_url(message_text, user)
        
        # Default: respond with AI or simple echo
        response_text = f"📝 Received: {message_text[:100]}\n\n"
        response_text += "I'm processing your message. For scraping, send me a URL."
        
        # Cache the response
        await cache_service.set(
            user_id=user.id,
            cache_key=cache_key,
            value={"message": response_text},
            ttl_seconds=self.cache_ttl
        )
        
        return ControllerResponse(
            success=True,
            message=response_text
        )

    # === Command Handlers ===

    async def _cmd_start(
        self,
        update: TelegramUpdate,
        user: User,
        user_state: Optional[Dict]
    ) -> ControllerResponse:
        """Handle /start command"""
        welcome_message = """
🤖 <b>Welcome to AmkyawDev AI Agent!</b>

I can help you with:
• 🌐 Web scraping - Send me any URL
• 📸 Screenshots - Capture web pages
• 💬 AI Chat - Ask me anything
• 🔧 And more!

<b>Quick Commands:</b>
/scrape [url] - Scrape webpage content
/screenshot [url] - Take a screenshot
/help - Show all commands
"""
        return ControllerResponse(
            success=True,
            message=welcome_message
        )

    async def _cmd_help(
        self,
        update: TelegramUpdate,
        user: User,
        user_state: Optional[Dict]
    ) -> ControllerResponse:
        """Handle /help command"""
        help_message = """
📚 <b>Available Commands</b>

<b>Web Scraping:</b>
/scrape [url] - Extract content from a webpage
/screenshot [url] - Take a screenshot

<b>Conversation:</b>
/history - View chat history
/clear - Clear current session

<b>Settings:</b>
/settings - Configure preferences

<b>Just type</b> any URL to scrape it automatically!
"""
        return ControllerResponse(
            success=True,
            message=help_message
        )

    async def _cmd_scrape(
        self,
        update: TelegramUpdate,
        user: User,
        user_state: Optional[Dict]
    ) -> ControllerResponse:
        """Handle /scrape command"""
        message = update.message_text.replace("/scrape", "").strip()
        
        if not message:
            return ControllerResponse(
                success=False,
                message="📋 <b>Usage:</b> /scrape [URL]\n\nExample: /scrape https://example.com"
            )
        
        if not self._is_url(message):
            return ControllerResponse(
                success=False,
                message="⚠️ Invalid URL. Please provide a valid URL starting with http:// or https://"
            )
        
        return await self._scrape_url(message, user)

    async def _cmd_screenshot(
        self,
        update: TelegramUpdate,
        user: User,
        user_state: Optional[Dict]
    ) -> ControllerResponse:
        """Handle /screenshot command"""
        message = update.message_text.replace("/screenshot", "").strip()
        
        if not message:
            return ControllerResponse(
                success=False,
                message="📸 <b>Usage:</b> /screenshot [URL]\n\nExample: /screenshot https://example.com"
            )
        
        if not self._is_url(message):
            return ControllerResponse(
                success=False,
                message="⚠️ Invalid URL. Please provide a valid URL."
            )
        
        # Check cache first
        cache_key = cache_service.generate_key("screenshot", message)
        cached = await cache_service.get(user.id, cache_key)
        if cached:
            return ControllerResponse(
                success=True,
                message="📸 Screenshot (cached)",
                data=cached
            )
        
        # Take screenshot
        try:
            with asyncio.timeout(self.browserless_timeout):
                result = await self.browserless.screenshot(message)
            
            if result.success and result.screenshot:
                # Store in cache
                await cache_service.set(
                    user_id=user.id,
                    cache_key=cache_key,
                    value={"screenshot": result.screenshot, "url": message},
                    ttl_seconds=self.cache_ttl
                )
                
                return ControllerResponse(
                    success=True,
                    message=f"📸 Screenshot captured for {message}",
                    data={"screenshot": result.screenshot}
                )
            else:
                return ControllerResponse(
                    success=False,
                    message=f"⚠️ Failed to capture screenshot: {result.error or 'Unknown error'}"
                )
                
        except asyncio.TimeoutError:
            return ControllerResponse(
                success=False,
                message="⏱️ Screenshot timed out. The website might be slow or unavailable."
            )
        except Exception as e:
            return ControllerResponse(
                success=False,
                message=f"⚠️ Error capturing screenshot: {str(e)}"
            )

    async def _cmd_history(
        self,
        update: TelegramUpdate,
        user: User,
        user_state: Optional[Dict]
    ) -> ControllerResponse:
        """Handle /history command"""
        async with db_manager.session() as session:
            query = (
                select(Conversation)
                .where(Conversation.user_id == user.id)
                .order_by(Conversation.updated_at.desc())
                .limit(10)
            )
            result = await session.execute(query)
            conversations = result.scalars().all()
        
        if not conversations:
            return ControllerResponse(
                success=True,
                message="📭 No conversation history yet."
            )
        
        history_text = "📜 <b>Recent Conversations:</b>\n\n"
        for conv in conversations:
            title = conv.title or f"Chat {conv.id}"
            date = conv.updated_at.strftime("%Y-%m-%d %H:%M")
            history_text += f"• {title} ({date})\n"
        
        return ControllerResponse(
            success=True,
            message=history_text
        )

    async def _cmd_clear(
        self,
        update: TelegramUpdate,
        user: User,
        user_state: Optional[Dict]
    ) -> ControllerResponse:
        """Handle /clear command"""
        # Clear user state
        await state_service.delete_state(user.id, "current_context")
        await state_service.delete_state(user.id, "pending_operation")
        
        # Clear cache
        await cache_service.clear_user_cache(user.id)
        
        return ControllerResponse(
            success=True,
            message="🧹 Session cleared! All cached data has been removed."
        )

    async def _cmd_settings(
        self,
        update: TelegramUpdate,
        user: User,
        user_state: Optional[Dict]
    ) -> ControllerResponse:
        """Handle /settings command"""
        settings_text = """
⚙️ <b>Settings</b>

<b>Cache TTL:</b> 1 hour
<b>State TTL:</b> 30 minutes

More settings coming soon!
"""
        return ControllerResponse(
            success=True,
            message=settings_text
        )

    # === Helper Methods ===

    async def _scrape_url(self, url: str, user: User) -> ControllerResponse:
        """Scrape URL using Browserless API"""
        # Check cache
        cache_key = cache_service.generate_key("scrape", url)
        cached = await cache_service.get(user.id, cache_key)
        if cached:
            return ControllerResponse(
                success=True,
                message="🌐 Scraped content (cached):\n\n" + cached.get("content", "")[:1000],
                data=cached
            )
        
        try:
            with asyncio.timeout(self.browserless_timeout):
                result = await self.browserless.scrape(url)
            
            if result.success and result.data:
                content = self._extract_text_from_scrape_data(result.data)
                
                # Cache the result
                await cache_service.set(
                    user_id=user.id,
                    cache_key=cache_key,
                    value={"url": url, "content": content},
                    ttl_seconds=self.cache_ttl
                )
                
                return ControllerResponse(
                    success=True,
                    message="🌐 <b>Scraped Content:</b>\n\n" + content[:1500],
                    data={"url": url, "content": content}
                )
            else:
                return ControllerResponse(
                    success=False,
                    message=f"⚠️ Failed to scrape: {result.error or 'Unknown error'}"
                )
                
        except asyncio.TimeoutError:
            raise BrowserlessError(
                message="Scraping timed out",
                details={"url": url},
                retry_after=120
            )

    async def _get_or_create_user(self, update: TelegramUpdate) -> Optional[User]:
        """Get existing user or create new one"""
        try:
            async with db_manager.session() as session:
                # Try to find by telegram_id
                if update.user_id:
                    query = select(User).where(User.telegram_id == str(update.user_id))
                    result = await session.execute(query)
                    user = result.scalar_one_or_none()
                    
                    if user:
                        return user
                
                # Create new user
                new_user = User(
                    telegram_id=str(update.user_id) if update.user_id else None,
                    username=update.username or f"user_{update.user_id}",
                    hashed_password="",  # Telegram users don't need password
                    is_active=True
                )
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
                
                logger.info(f"Created new user: {new_user.id}")
                return new_user
                
        except Exception as e:
            logger.error(f"Error getting/creating user: {e}")
            return None

    def _is_url(self, text: str) -> bool:
        """Check if text is a valid URL"""
        text = text.strip().lower()
        return text.startswith("http://") or text.startswith("https://")

    def _extract_text_from_scrape_data(self, data: Dict) -> str:
        """Extract clean text from scrape result"""
        if not data:
            return "No content extracted"
        
        # Try common content extraction
        content = data.get("text") or data.get("content") or data.get("data", {})
        
        if isinstance(content, dict):
            content = content.get("text", str(content))
        
        if isinstance(content, list):
            content = " ".join(str(item) for item in content)
        
        return str(content)[:2000]


# Singleton controller instance
controller = Controller()
