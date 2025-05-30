from aiogram import types, Dispatcher
from helpers.sambutan import kirim_sambutan

async def start_handler(message: types.Message):
    kirim_sambutan(message)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
#     dp.register_message_handler(start_handler, commands=["help"])