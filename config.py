import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SHEET_ID = os.getenv("SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")


