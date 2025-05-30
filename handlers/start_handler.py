# handlers/start_handler.py
from aiogram import types, Dispatcher
from helpers.sambutan import kirim_sambutan

async def start_command_handler(message: types.Message):
    print(">>> /start received")  # DEBUG LOG
    await kirim_sambutan(message)

def register_handlers(dp: Dispatcher):
    print("__ start_handler registered")  # DEBUG LOG
    dp.register_message_handler(start_command_handler, commands=["start"])
