"""
Webhook Routes
==============
FastAPI routes for handling webhooks (Telegram, etc.)
"""

import logging
import asyncio
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException, Header, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.config import settings
from app.services.telegram_service import create_telegram_bot, TelegramBot

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhooks"])

# Global bot instance
_telegram_bot: Optional[TelegramBot] = None


async def get_telegram_bot() -> TelegramBot:
    """Get or create Telegram bot instance"""
    global _telegram_bot
    if _telegram_bot is None:
        _telegram_bot = create_telegram_bot(
            webhook_host=settings.WEBHOOK_HOST
        )
    return _telegram_bot


class WebhookResponse(BaseModel):
    """Standard webhook response"""
    status: str
    message: Optional[str] = None
    timestamp: datetime = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Update processed",
                "timestamp": "2025-01-15T10:30:00Z"
            }
        }


@router.post("/telegram", response_model=WebhookResponse)
async def telegram_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_telegram_bot_api_secret_token: Optional[str] = Header(None, alias="X-Telegram-Bot-Api-Secret-Token")
):
    """
    Telegram webhook endpoint
    
    Receives updates from Telegram and processes them asynchronously
    """
    try:
        # Verify secret token (if configured)
        if settings.TELEGRAM_WEBHOOK_SECRET:
            if x_telegram_bot_api_secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
                logger.warning("Invalid Telegram webhook secret")
                raise HTTPException(status_code=403, detail="Forbidden")
        
        # Parse update
        update_dict = await request.json()
        update_id = update_dict.get("update_id", "unknown")
        
        logger.info(f"Received Telegram update: {update_id}")
        
        # Process in background to respond quickly
        async def process_update():
            try:
                bot = await get_telegram_bot()
                await bot.process_webhook_update(update_dict)
            except Exception as e:
                logger.error(f"Error processing Telegram update: {e}")
        
        background_tasks.add_task(process_update)
        
        # Return immediately to acknowledge receipt
        return WebhookResponse(
            status="success",
            message=f"Update {update_id} queued for processing",
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        return WebhookResponse(
            status="error",
            message=str(e),
            timestamp=datetime.utcnow()
        )


@router.get("/telegram/info", response_model=WebhookResponse)
async def telegram_webhook_info():
    """Get Telegram webhook info"""
    try:
        bot = await get_telegram_bot()
        info = await bot.get_webhook_info()
        
        return JSONResponse({
            "status": "success",
            "data": info,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/telegram/set", response_model=WebhookResponse)
async def telegram_set_webhook():
    """Set Telegram webhook URL"""
    try:
        if not settings.WEBHOOK_HOST:
            raise HTTPException(
                status_code=400,
                detail="WEBHOOK_HOST not configured"
            )
        
        bot = await get_telegram_bot()
        success = await bot.set_webhook()
        
        if success:
            return WebhookResponse(
                status="success",
                message="Webhook set successfully",
                timestamp=datetime.utcnow()
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to set webhook"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/telegram", response_model=WebhookResponse)
async def telegram_delete_webhook():
    """Delete Telegram webhook"""
    try:
        bot = await get_telegram_bot()
        success = await bot.delete_webhook()
        
        if success:
            return WebhookResponse(
                status="success",
                message="Webhook deleted",
                timestamp=datetime.utcnow()
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete webhook"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# === Generic Webhook Handler ===

class GenericWebhookPayload(BaseModel):
    """Generic webhook payload"""
    source: str
    event_type: str
    data: dict
    timestamp: Optional[datetime] = None


@router.post("/generic/{source}", response_model=WebhookResponse)
async def generic_webhook(
    source: str,
    payload: GenericWebhookPayload,
    background_tasks: BackgroundTasks
):
    """
    Generic webhook handler for custom integrations
    """
    logger.info(f"Received webhook from {source}: {payload.event_type}")
    
    # Log webhook for debugging
    from app.database.connection import db_manager
    from app.database.models import WebhookLog
    
    async def log_webhook():
        try:
            async with db_manager.session() as session:
                log = WebhookLog(
                    source=source,
                    event_type=payload.event_type,
                    payload=payload.data,
                    status="pending"
                )
                session.add(log)
                # Don't commit - let it be async
        
        except Exception as e:
            logger.error(f"Failed to log webhook: {e}")
    
    background_tasks.add_task(log_webhook)
    
    return WebhookResponse(
        status="success",
        message=f"Webhook from {source} received",
        timestamp=datetime.utcnow()
    )
