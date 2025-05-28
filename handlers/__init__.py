from .list_handler import list_done, list_pending
from telegram.ext import Application

def register_all_handlers(app: Application):
    app.add_handler(list_done)
    app.add_handler(list_pending)
