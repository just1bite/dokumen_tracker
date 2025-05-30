from aiogram import Bot, Dispatcher, executor, types
from config import TELEGRAM_BOT_TOKEN
from handlers import register_handlers
from sheet.sheet_services import sync_memos_to_tracker
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

register_handlers(dp)

async def on_startup(dispatcher):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, sync_memos_to_tracker)
    logging.info("🤖 Bot started and MEMO synced to Tracker.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
