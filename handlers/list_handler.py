from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sheet.sheet_services import get_all_tracker_data

async def list_command_handler(message: types.Message):
    args = message.get_args().strip().lower()
    data = get_all_tracker_data()

    if args == "pending":
        data = [row for row in data if row["Status"] != "done"]
    elif args == "done":
        data = [row for row in data if row["Status"] == "done"]

    if not data:
        await message.reply("❌ Tidak ada dokumen yang sesuai filter.")
        return

    keyboard = InlineKeyboardMarkup(row_width=1)
    for row in data:
        label = f"{row['No Document']} - {row['Nama Document']} ({row['Status']})"
        keyboard.add(
            InlineKeyboardButton(
                text=label,
                callback_data=f"detail_doc|{row['No Document']}"
            )
        )

    if args == "pending":
        title = "📋 Daftar dokumen *belum selesai*:"
    elif args == "done":
        title = "📋 Daftar dokumen *selesai*:"
    else:
        title = "📋 Daftar *semua dokumen*:"

    await message.reply(title, reply_markup=keyboard, parse_mode="Markdown")

async def document_detail_callback(callback: types.CallbackQuery):
    _, doc_id = callback.data.split("|")
    data = get_all_tracker_data()

    detail = next((row for row in data if row["No Document"] == doc_id), None)
    if not detail:
        await callback.message.reply("❌ Dokumen tidak ditemukan.")
        return

    message = f"""
📄 *Detail Dokumen*
*No:* {detail['No Document']}
*Nama:* {detail['Nama Document']}
*Status:* `{detail['Status']}`
*Note:* {detail.get('Note', '-') or '-'}
*Last Updated:* {detail.get('Last Updated', '-') or '-'}
*History:* 
""".strip()

    await callback.message.answer(message, parse_mode="Markdown")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(list_command_handler, commands=["list"])
    dp.register_callback_query_handler(document_detail_callback, lambda c: c.data.startswith("detail_doc"))
