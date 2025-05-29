from aiogram import Bot, Dispatcher, executor, types
from config import TELEGRAM_BOT_TOKEN, SHEET_ID, SHEET_NAME, CREDENTIALS_FILE
from handlers import register_handlers
import logging

# Logging
logging.basicConfig(level=logging.INFO)

# Bot & Dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Register all handlers
register_handlers(dp)

# Fungsi ketika bot ready
async def on_startup(dispatcher):
    from sheet.sheet_services import sync_memos_to_tracker
    sync_memos_to_tracker()
    logging.info("🤖 Bot started and MEMO synced to Tracker.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
