from telebot.types import Message
from config import bot
from .markdown_util import escape_markdown_v2

def kirim_sambutan(message: Message):
    text = (
        "👋 *Selamat datang di document_tracker Bot!*\n\n"
        "Bot ini digunakan untuk melakukan update progres approval dokumen & traking document.\n\n"
        "*Perintah yang tersedia:*\n"
        "📌 /list — untuk melihat daftar dokumen\n"
        "📌 /list keyword — untuk mencari didaftar dokumen\n"
        "📌 /update — untuk update data approval dokumen\n"
        "Jika ingin melakukan update untuk pertama kali, silahkan gunakan perintah /chat_id kirim chat_id ke admin terima kasih!"
    )
    bot.send_message(message.chat.id, escape_markdown_v2(text), parse_mode="MarkdownV2")
