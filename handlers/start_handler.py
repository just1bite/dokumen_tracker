from aiogram import types, Dispatcher
from helpers.sambutan import kirim_sambutan

async def start_command_handler(message: types.Message):
    await kirim_sambutan(message)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command_handler, commands=["start"])
