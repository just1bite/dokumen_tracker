import re
from datetime import datetime, timedelta
from sheet.sheet_google import get_sheet, get_all_memo_data, get_all_tracker_data, append_to_tracker, update_row

# Sinkronisasi Memo → Tracker
def sync_memos_to_tracker():
    memo_data = get_all_memo_data()
    tracker_data = get_all_tracker_data()

    existing_docs = {row['No Document'] for row in tracker_data}

    new_docs = []
    for row in memo_data:
        nomor = row['Nomor'].strip()
        if nomor not in existing_docs and re.match(r".*/2025$", nomor):
            new_docs.append([
                nomor,                   # No Document
                row['Deskripsi'],       # Nama Document
                "",                     # Status
                ""                      # Note
            ])

    if new_docs:
        append_to_tracker(new_docs)


def get_pending_documents():
    data = get_all_tracker_data()
    return [
        row for row in data
        if row.get('Status', '').strip().lower() != 'done'
    ]


def update_document_status(doc_id, new_status, note, updated_by):
    ws = get_sheet("Tracker")
    all_data = ws.get_all_values()
    headers = all_data[0]

    try:
        note_col = headers.index("Note")
        status_col = headers.index("Status")
        updated_col = headers.index("Last Updated")
        history_col = headers.index("History") if "History" in headers else -1
    except ValueError as e:
        raise Exception("❌ Kolom tidak ditemukan di header: " + str(e))

    for i, row in enumerate(all_data[1:], start=2):
        if row[0].strip() == doc_id:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            ws.update_cell(i, status_col + 1, new_status)
            ws.update_cell(i, note_col + 1, note)
            ws.update_cell(i, updated_col + 1, now)

            if history_col != -1:
                old_history = row[history_col] if len(row) > history_col else ""
                new_entry = f"{new_status} by {updated_by} at {now}"
                updated_history = f"{old_history}\n{new_entry}".strip()
                ws.update_cell(i, history_col + 1, updated_history)
            break
def get_document_by_id(doc_id):
    data = get_all_tracker_data()
    for row in data:
        if row.get("No Document", "").strip() == doc_id.strip():
            return row
    return None

def auto_complete_documents():
    data =  get_all_tracker_data()

    for index, row in enumerate(data):
        status = row.get("Status", "").strip().lower()
        last_updated_str = row.get("Last Updated", "").strip()

        # Lewatkan jika bukan akunting atau tidak ada tanggal
        if status != "akunting" or not last_updated_str:
            continue

        try:
            last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d")
        except ValueError:
            continue  # Lewatkan jika format salah

        if datetime.now() - last_updated >= timedelta(days=14):
            # Update status jadi done by system
            update_row(index + 2, {
                "Status": "done",
                "Note": "✅ Auto done by system after 14 days",
                "Last Updated": datetime.now().strftime("%Y-%m-%d"),
                "History": f"{row.get('History', '')}\nAuto updated on {datetime.now().strftime('%Y-%m-%d')} by system"
            })
def add_document_to_tracker(doc: dict):
    try:
        print(f"Menambahkan dokumen ke tracker: {doc}")
        sheet = get_sheet("Tracker")

        headers = sheet.row_values(1)
        row_data = [doc.get(header, "") for header in headers]

        print("Row yang akan ditambahkan:", row_data)
        sheet.append_row(row_data, value_input_option="USER_ENTERED")
        print("Baris sudah ditambahkan ke sheet")
    except Exception as e:
        print("Gagal menambahkan dokumen:", e)
