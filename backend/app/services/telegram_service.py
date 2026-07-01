"""
Telegram Bot Service (aiogram v3)
================================
Webhook-based Telegram bot with async integration
"""

import logging
import asyncio
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass, field

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Update, Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.exceptions import AiogramError, TelegramAPIError
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.controllers.orchestrator import Controller, TelegramUpdate, ControllerResponse
from app.middleware.error_handler import error_handler

logger = logging.getLogger(__name__)


class TelegramBot:
    """
    Telegram Bot with webhook support
    Integrates with the Controller orchestrator
    """
    
    def __init__(
        self,
        token: Optional[str] = None,
        controller: Optional[Controller] = None,
        webhook_host: Optional[str] = None
    ):
        self.token = token or settings.TELEGRAM_BOT_TOKEN
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        
        # Initialize bot with default properties
        self.bot = Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        # Initialize dispatcher with memory storage for FSM
        self.dp = Dispatcher(storage=MemoryStorage())
        
        # Set up controller
        self.controller = controller
        
        # Webhook settings
        self.webhook_host = webhook_host
        self.webhook_path = "/webhook/telegram"
        self.secret_token = "telegram_webhook_secret"  # Should be randomized in production
        
        # Setup router
        self.router = Router()
        self._setup_handlers()
        self.dp.include_router(self.router)
        
        # Connect error handler to bot
        error_handler.set_telegram_bot(self.bot)
        
        logger.info("Telegram bot initialized")

    def _setup_handlers(self) -> None:
        """Setup message and command handlers"""
        
        @self.router.message(CommandStart())
        async def cmd_start(message: Message, state: FSMContext):
            await self._handle_command_start(message, state)
        
        @self.router.message(Command("help"))
        async def cmd_help(message: Message):
            await self._handle_help(message)
        
        @self.router.message(Command("scrape"))
        async def cmd_scrape(message: Message):
            await self._handle_scrape_command(message)
        
        @self.router.message(Command("screenshot"))
        async def cmd_screenshot(message: Message):
            await self._handle_screenshot_command(message)
        
        @self.router.message(Command("history"))
        async def cmd_history(message: Message):
            await self._handle_history_command(message)
        
        @self.router.message(Command("clear"))
        async def cmd_clear(message: Message):
            await self._handle_clear_command(message)
        
        @self.router.message(F.text)
        async def handle_text(message: Message, state: FSMContext):
            await self._handle_text_message(message, state)
        
        @self.router.message(F.photo)
        async def handle_photo(message: Message):
            await message.reply("📷 Photo received. I can process images soon!")
        
        @self.router.message(F.document)
        async def handle_document(message: Message):
            await message.reply("📄 Document received. I'll save it shortly!")

    async def _handle_command_start(self, message: Message, state: FSMContext):
        """Handle /start command"""
        await state.clear()
        
        update = TelegramUpdate(
            update_id=message.update_id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            chat_id=message.chat.id,
            command="/start"
        )
        
        if self.controller:
            response = await self.controller.process_update(update)
        else:
            response = await self._default_start_response()
        
        await message.reply(response.message, parse_mode=ParseMode.HTML)

    async def _handle_help(self, message: Message):
        """Handle /help command"""
        update = TelegramUpdate(
            update_id=message.update_id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            chat_id=message.chat.id,
            command="/help"
        )
        
        if self.controller:
            response = await self.controller.process_update(update)
        else:
            response = await self._default_help_response()
        
        await message.reply(response.message, parse_mode=ParseMode.HTML)

    async def _handle_scrape_command(self, message: Message):
        """Handle /scrape command"""
        url = message.text.replace("/scrape", "").strip()
        
        update = TelegramUpdate(
            update_id=message.update_id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            chat_id=message.chat.id,
            message_text=f"/scrape {url}" if url else "/scrape",
            command="/scrape" if not url else None
        )
        
        # Send typing indicator
        await message.chat.do("typing")
        
        if self.controller:
            response = await self.controller.process_update(update)
        else:
            response = ControllerResponse(
                success=False,
                message="Controller not configured"
            )
        
        await message.reply(response.message, parse_mode=ParseMode.HTML)

    async def _handle_screenshot_command(self, message: Message):
        """Handle /screenshot command"""
        url = message.text.replace("/screenshot", "").strip()
        
        if url:
            update = TelegramUpdate(
                update_id=message.update_id,
                user_id=message.from_user.id,
                username=message.from_user.username,
                chat_id=message.chat.id,
                message_text=url
            )
            
            await message.chat.do("typing")
            
            if self.controller:
                response = await self.controller.process_update(update)
                
                # Send photo if screenshot available
                if response.data and response.data.get("screenshot"):
                    import base64
                    from io import BytesIO
                    from PIL import Image
                    
                    screenshot_data = response.data["screenshot"]
                    if "," in screenshot_data:  # Handle base64 data URI
                        screenshot_data = screenshot_data.split(",")[1]
                    
                    image_bytes = base64.b64decode(screenshot_data)
                    await message.reply_photo(
                        photo=BytesIO(image_bytes),
                        caption=response.message
                    )
                    return
            
            await message.reply(response.message, parse_mode=ParseMode.HTML)
        else:
            await message.reply(
                "📸 <b>Usage:</b> /screenshot [URL]\n\n"
                "Example: /screenshot https://example.com",
                parse_mode=ParseMode.HTML
            )

    async def _handle_history_command(self, message: Message):
        """Handle /history command"""
        update = TelegramUpdate(
            update_id=message.update_id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            chat_id=message.chat.id,
            command="/history"
        )
        
        if self.controller:
            response = await self.controller.process_update(update)
        else:
            response = ControllerResponse(
                success=True,
                message="📭 No history available (controller not configured)"
            )
        
        await message.reply(response.message, parse_mode=ParseMode.HTML)

    async def _handle_clear_command(self, message: Message):
        """Handle /clear command"""
        update = TelegramUpdate(
            update_id=message.update_id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            chat_id=message.chat.id,
            command="/clear"
        )
        
        if self.controller:
            response = await self.controller.process_update(update)
        else:
            response = ControllerResponse(
                success=True,
                message="🧹 Session cleared"
            )
        
        await message.reply(response.message, parse_mode=ParseMode.HTML)

    async def _handle_text_message(self, message: Message, state: FSMContext):
        """Handle regular text messages"""
        # Check if message is a command without handler
        if message.text.startswith("/"):
            await message.reply(
                "❓ Unknown command. Type /help for available commands.",
                parse_mode=ParseMode.HTML
            )
            return
        
        update = TelegramUpdate(
            update_id=message.update_id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            chat_id=message.chat.id,
            message_text=message.text
        )
        
        # Send typing indicator
        await message.chat.do("typing")
        
        if self.controller:
            response = await self.controller.process_update(update)
        else:
            response = await self._default_text_response(message.text)
        
        await message.reply(response.message, parse_mode=ParseMode.HTML)

    # === Default Responses ===

    async def _default_start_response(self) -> ControllerResponse:
        """Default /start response"""
        return ControllerResponse(
            success=True,
            message="""
🤖 <b>Welcome to AmkyawDev AI Agent!</b>

I'm here to help you with web scraping and automation.

<b>Commands:</b>
/scrape [url] - Extract content from webpage
/screenshot [url] - Take a screenshot
/history - View chat history
/clear - Clear session
/help - Show all commands

Just send me a URL to scrape it!
"""
        )

    async def _default_help_response(self) -> ControllerResponse:
        """Default /help response"""
        return ControllerResponse(
            success=True,
            message="""
📚 <b>Available Commands</b>

<b>Web Scraping:</b>
/scrape [url] - Extract webpage content
/screenshot [url] - Capture screenshot

<b>General:</b>
/history - View conversation history
/clear - Clear current session
/help - Show this help

<b>Tip:</b> Send any URL to scrape it automatically!
"""
        )

    async def _default_text_response(self, text: str) -> ControllerResponse:
        """Default text message response"""
        text_lower = text.lower().strip()
        
        if text_lower.startswith("http://") or text_lower.startswith("https://"):
            return ControllerResponse(
                success=True,
                message=f"🌐 I see you sent a URL: {text}\n\nUse /scrape {text} to extract content or /screenshot {text} to take a screenshot."
            )
        
        return ControllerResponse(
            success=True,
            message=f"👋 I received your message: {text[:100]}\n\nType /help for available commands."
        )

    # === Webhook Management ===

    async def set_webhook(self) -> bool:
        """Set webhook URL with Telegram"""
        if not self.webhook_host:
            logger.warning("Webhook host not configured")
            return False
        
        webhook_url = f"{self.webhook_host.rstrip('/')}{self.webhook_path}"
        
        try:
            await self.bot.set_webhook(
                url=webhook_url,
                secret_token=self.secret_token,
                allowed_updates=["message", "callback_query"]
            )
            logger.info(f"Webhook set to: {webhook_url}")
            return True
        except AiogramError as e:
            logger.error(f"Failed to set webhook: {e}")
            return False

    async def delete_webhook(self) -> bool:
        """Delete webhook"""
        try:
            await self.bot.delete_webhook()
            logger.info("Webhook deleted")
            return True
        except AiogramError as e:
            logger.error(f"Failed to delete webhook: {e}")
            return False

    async def get_webhook_info(self) -> Dict[str, Any]:
        """Get current webhook info"""
        try:
            info = await self.bot.get_webhook_info()
            return {
                "url": info.url,
                "has_custom_certificate": info.has_custom_certificate,
                "pending_update_count": info.pending_update_count,
                "last_error_date": info.last_error_date,
                "last_error_message": info.last_error_message
            }
        except AiogramError as e:
            logger.error(f"Failed to get webhook info: {e}")
            return {"error": str(e)}

    async def process_webhook_update(self, update_dict: Dict[str, Any]) -> None:
        """
        Process incoming webhook update
        
        Args:
            update_dict: Parsed JSON update from Telegram webhook
        """
        try:
            update = Update.model_validate(update_dict)
            await self.dp.feed_update(self.bot, update)
        except Exception as e:
            logger.error(f"Error processing webhook update: {e}")
            await error_handler.handle_error(
                e,
                context={"source": "telegram_webhook"}
            )

    async def start_polling(self) -> None:
        """Start bot using polling (for development)"""
        logger.info("Starting bot with polling...")
        try:
            await self.dp.start_polling(
                self.bot,
                allowed_updates=["message", "callback_query"]
            )
        finally:
            await self.bot.session.close()

    async def close(self) -> None:
        """Close bot sessions"""
        await self.dp.storage.close()
        await self.bot.session.close()
        logger.info("Telegram bot closed")


# Factory function
def create_telegram_bot(
    token: Optional[str] = None,
    webhook_host: Optional[str] = None
) -> TelegramBot:
    """Create configured Telegram bot"""
    from app.controllers.orchestrator import controller as app_controller
    
    return TelegramBot(
        token=token,
        controller=app_controller,
        webhook_host=webhook_host
    )
