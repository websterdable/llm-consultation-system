from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.core.config import settings
from app.bot.handlers import router

bot = Bot(token=settings.telegram_bot_token, default=DefaultBotProperties())
dp = Dispatcher()
dp.include_router(router)