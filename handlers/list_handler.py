from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from sheet.sheet_services import ambil_dokumen_berdasarkan_status

async def handle_list_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = ambil_dokumen_berdasarkan_status("done")
    await _send_list_response(update, data, "done")

async def handle_list_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = ambil_dokumen_berdasarkan_status("done", exclude=True)
    await _send_list_response(update, data, "pending")

async def _send_list_response(update: Update, data, label: str):
    if not data:
        await update.message.reply_text(f"📭 Tidak ada dokumen dengan status {label}.")
        return

    max_rows = 15
    limited_data = data[:max_rows]

    pesan = "\n".join(
        [f"{i+1}. {' | '.join(row)}" for i, row in enumerate(limited_data)]
    )
    if len(data) > max_rows:
        pesan += f"\n\n📄 Ditampilkan {max_rows} dari {len(data)} data."

    await update.message.reply_text(pesan)

# Handler objects to be registered
list_done = CommandHandler("list_done", handle_list_done)
list_pending = CommandHandler("list_pending", handle_list_pending)
