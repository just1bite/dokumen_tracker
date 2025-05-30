from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sheet.sheet_services import get_pending_documents, update_document_status, get_document_by_id, sync_memos_to_tracker


# Simpan state sederhana sementara (untuk produksi sebaiknya pakai FSM)
user_state = {}

async def update_command_handler(message: types.Message):
    sync_memos_to_tracker()
    all_docs = get_pending_documents()

    pending_docs = [
    doc for doc in all_docs
    if doc["No Document"].strip().endswith("/2025")
    ]

    
    if not pending_docs:
        await message.reply("✅ Semua dokumen telah diproses.")
        return

    MAX_BUTTONS_PER_MESSAGE = 40
    chunks = [pending_docs[i:i + MAX_BUTTONS_PER_MESSAGE] for i in range(0, len(pending_docs), MAX_BUTTONS_PER_MESSAGE)]

    for i, chunk in enumerate(chunks):
        keyboard = InlineKeyboardMarkup()
        for doc in chunk:
            btn = InlineKeyboardButton(
                text=f"{doc['No Document']} - {doc['Nama Document']}",
                callback_data=f"select_doc|{doc['No Document']}"
            )
            keyboard.add(btn)

        await message.reply(
            f"📋 Pilih dokumen yang ingin diupdate (Batch {i + 1}/{len(chunks)}):",
            reply_markup=keyboard
        )

async def select_document_callback(callback: types.CallbackQuery):
    _, doc_id = callback.data.split("|")
    doc = get_document_by_id(doc_id)

    if not doc:
        await callback.message.edit_text("❌ Dokumen tidak ditemukan.")
        return

    current_status = doc.get("Status", "").strip().lower()
    user_state[callback.from_user.id] = {"doc_id": doc_id}

    # Tentukan opsi berdasarkan status saat ini
    available_statuses = []
    if current_status == "":
        available_statuses = ["management", "akunting", "done"]
    elif current_status == "management":
        available_statuses = ["akunting", "done"]
    elif current_status == "akunting":
        available_statuses = ["done"]

    # Buat tombol sesuai opsi
    keyboard = InlineKeyboardMarkup(row_width=2)
    for status in available_statuses:
        keyboard.insert(
            InlineKeyboardButton(text=status.capitalize(), callback_data=f"select_status|{status}")
        )

    await callback.message.edit_text(
        f"📝 Pilih status baru untuk dokumen {doc_id} (saat ini: <b>{current_status or 'Belum ada'}</b>):",
        reply_markup=keyboard
    )


async def select_status_callback(callback: types.CallbackQuery):
    _, status = callback.data.split("|")
    uid = callback.from_user.id
    user_state[uid]["status"] = status

    await callback.message.edit_text("🗒 Silakan masukkan note (atau ketik `-` jika kosong):")

async def text_handler(message: types.Message):
    uid = message.from_user.id
    if uid not in user_state or "status" not in user_state[uid]:
        return

    note = message.text if message.text.strip() != "-" else ""
    doc_id = user_state[uid]["doc_id"]
    status = user_state[uid]["status"]
    username = message.from_user.full_name

    update_document_status(doc_id, status, note, username)

    await message.reply(f"✅ Dokumen *{doc_id}* berhasil diupdate ke *{status}*", parse_mode="Markdown")
    user_state.pop(uid) 

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(update_command_handler, commands=["update"])
    dp.register_callback_query_handler(select_document_callback, lambda c: c.data.startswith("select_doc"))
    dp.register_callback_query_handler(select_status_callback, lambda c: c.data.startswith("select_status"))
    dp.register_message_handler(text_handler, content_types=types.ContentTypes.TEXT)


