# helpers/sambutan.py
from aiogram import types

async def kirim_sambutan(message: types.Message):
    text = (
        "👋 <b>Selamat datang di Document Tracker Bot!</b>\n\n"
        "Bot ini digunakan untuk tracking dan approval dokumen.\n\n"
        "<b>Perintah:</b>\n"
        "📌 /list — melihat semua daftar dokumen\n"
        "📌 /pending — update approval dokumen yang sedang berjalan\n"
        "📌 /list keyword — cari dokumen sesuai dengan keyword contoh: 69/MEM-IT/2025\n"
        "📌 /start — sambutan ini\n\n"
    )
    await message.answer(text, parse_mode="HTML")
