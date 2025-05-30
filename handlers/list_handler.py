from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sheet.sheet_services import get_all_tracker_data

ITEMS_PER_PAGE = 10

def filter_data(data, filter_name):
    if filter_name == "pending":
        return [row for row in data if row["Status"].lower() != "done"]
    elif filter_name == "done":
        return [row for row in data if row["Status"].lower() == "done"]
    return data

def build_keyboard(data, page, filter_name):
    keyboard = InlineKeyboardMarkup(row_width=1)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_items = data[start:end]

    for row in page_items:
        label = f"{row['No Document']} - {row['Nama Document']} ({row['Status']})"
        keyboard.add(
            InlineKeyboardButton(
                text=label,
                callback_data=f"detail_doc|{row['No Document']}"
            )
        )

    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton("⬅️ Prev", callback_data=f"list_page|{page-1}|{filter_name}")
        )
    if end < len(data):
        nav_buttons.append(
            InlineKeyboardButton("Next ➡️", callback_data=f"list_page|{page+1}|{filter_name}")
        )
    if nav_buttons:
        keyboard.row(*nav_buttons)

    return keyboard

async def list_command_handler(message: types.Message):
    args = message.get_args().strip().lower()
    if args not in ["pending", "done"]:
        args = "all"

    data = get_all_tracker_data()
    filtered_data = filter_data(data, args)

    if not filtered_data:
        await message.reply("❌ Tidak ada dokumen yang sesuai filter.")
        return

    keyboard = build_keyboard(filtered_data, 0, args)
    title_map = {
        "all": "📋 Daftar *semua dokumen*:",
        "pending": "📋 Daftar dokumen *belum selesai*:",
        "done": "📋 Daftar dokumen *selesai*:",
    }
    title = title_map.get(args, "📋 Daftar dokumen:")

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

# callback untuk detail_doc tetap sama seperti sebelumnya, tinggal daftar di register_handlers

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(list_command_handler, commands=["list"])
    dp.register_callback_query_handler(list_page_callback, lambda c: c.data.startswith("list_page"))
    dp.register_callback_query_handler(document_detail_callback, lambda c: c.data.startswith("detail_doc"))
