from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sheet.sheet_services import add_document_to_tracker
from handlers.pending_handler import pending_command_handler, select_document_callback, select_status_callback, text_handler

# Simpan state sederhana sementara (untuk produksi sebaiknya pakai FSM)
user_state = {}

async def add_document_command_handler(message: types.Message):
    user_state[message.from_user.id] = {"mode": "adding"}
    await message.reply("📝 Masukkan *Nama Document* (boleh singkat):", parse_mode="Markdown")
async def handle_add_name(message: types.Message):
    uid = message.from_user.id
    if uid not in user_state or user_state[uid].get("mode") != "adding":
        return

    user_state[uid]["nama_doc"] = message.text.strip()

    keyboard = InlineKeyboardMarkup(row_width=2)
    for status in ["management", "akunting", "done"]:
        keyboard.insert(
            InlineKeyboardButton(text=status.capitalize(), callback_data=f"add_status|{status}")
        )

    await message.reply("📌 Pilih status dokumen:", reply_markup=keyboard)
async def add_status_callback(callback: types.CallbackQuery):
    _, status = callback.data.split("|")
    uid = callback.from_user.id
    user_state[uid]["status"] = status

    await callback.message.edit_text("✍️ Masukkan *Note* (atau ketik - jika kosong):", parse_mode="Markdown")
async def handle_add_note(message: types.Message):
    uid = message.from_user.id
    state = user_state.get(uid, {})
    if not state or state.get("mode") != "adding" or "status" not in state:
        return

    note = message.text if message.text.strip() != "-" else ""
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_doc = {
        "No Document": "",  # dikosongkan
        "Nama Document": state["nama_doc"],
        "Status": state["status"],
        "Note": note,
        "Last Updated": now,
        "History": f"Ditambahkan oleh {message.from_user.full_name} pada {now}"
    }

    from sheet.sheet_services import add_document_to_tracker
    add_document_to_tracker(new_doc)

    await message.reply(f"✅ Dokumen *{new_doc['Nama Document']}* berhasil ditambahkan dengan status *{new_doc['Status']}*.", parse_mode="Markdown")
    user_state.pop(uid)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(pending_command_handler, commands=["pending"])
    dp.register_message_handler(add_document_command_handler, commands=["add"])

    dp.register_callback_query_handler(select_document_callback, lambda c: c.data.startswith("select_doc"))
    dp.register_callback_query_handler(select_status_callback, lambda c: c.data.startswith("select_status"))
    dp.register_callback_query_handler(add_status_callback, lambda c: c.data.startswith("add_status"))

    # Handler untuk proses add (yang spesifik)
    dp.register_message_handler(handle_add_note,
        lambda m: not m.text.startswith("/") and m.from_user.id in user_state and user_state[m.from_user.id].get("mode") == "adding" and "status" in user_state[m.from_user.id])
    
    dp.register_message_handler(handle_add_name,
        lambda m: not m.text.startswith("/") and m.from_user.id in user_state and user_state[m.from_user.id].get("mode") == "adding" and "status" not in user_state[m.from_user.id])
    
    # Handler general untuk "pending" (paling bawah)
    dp.register_message_handler(text_handler,
        lambda m: not m.text.startswith("/") and m.from_user.id in user_state and user_state[m.from_user.id].get("mode") == "pending")