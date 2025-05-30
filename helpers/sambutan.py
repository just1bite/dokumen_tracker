from aiogram import types  # gunakan ini, bukan telebot

async def kirim_sambutan(message: types.Message):
    text = (
        "👋 <b>Selamat datang di Document Tracker Bot!</b>\n\n"
        "Bot ini digunakan untuk tracking dan approval dokumen.\n\n"
        "<b>Perintah:</b>\n"
        "📌 /list — melihat daftar dokumen\n"
        "📌 /update — update approval dokumen\n"
        "📌 /list keyword — cari dokumen\n"
        "📌 /start — sambutan ini\n\n"
    )
    await message.answer(text, parse_mode="HTML")
