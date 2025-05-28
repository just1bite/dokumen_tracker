from telegram.ext import ApplicationBuilder
from config import TELEGRAM_BOT_TOKEN
from handlers import register_all_handlers

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    register_all_handlers(app)
    app.run_polling()

if __name__ == "__main__":
    main()
