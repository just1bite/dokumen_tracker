from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from sheet.sheet_services import ambil_data_memo, tambah_ke_tracker, cek_sudah_ada

async def handle_add_memo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❗ Format salah. Gunakan:\n/add_memo <nomor> <status> [note opsional]")
        return

    nomor = context.args[0]
    status = context.args[1]
    note = " ".join(context.args[2:]) if len(context.args) > 2 else ""

    # Cek apakah sudah ada di Tracker
    if cek_sudah_ada(nomor):
        await update.message.reply_text(f"⚠️ Nomor dokumen {nomor} sudah ada di Tracker.")
        return

    # Ambil dari Sheet Memo
    data_memo = ambil_data_memo(nomor)
    if not data_memo:
        await update.message.reply_text(f"❌ Nomor {nomor} tidak ditemukan di sheet Memo.")
        return

    deskripsi = data_memo["Deskripsi"]
    tambah_ke_tracker(nomor, deskripsi, status, note)

    await update.message.reply_text(f"✅ Dokumen {nomor} berhasil ditambahkan ke Tracker.")

# Handler untuk registrasi
add_memo = CommandHandler("add_memo", handle_add_memo)
