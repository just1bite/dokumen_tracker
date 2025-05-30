import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Inisialisasi koneksi Google Sheet
def get_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    sheet_id = os.getenv("SHEET_ID")
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    return worksheet

# Ambil semua data dari Memo
def get_all_memo_data():
    ws = get_sheet("MEMO")
    rows = ws.get_all_records()
    return rows

# Ambil semua data dari Tracker
def get_all_tracker_data():
    ws = get_sheet("Tracker")
    rows = ws.get_all_records()
    return rows

# Tambahkan baris baru ke Tracker
def append_to_tracker(rows):
    ws = get_sheet("Tracker")
    ws.append_rows(rows, value_input_option="USER_ENTERED")

# Sinkronisasi Memo → Tracker
def sync_memo_to_tracker():
    memo_data = get_all_memo_data()  # ambil semua data dari Sheet Memo

    tracker_data = get_all_tracker_data()  # ambil semua data dari Tracker untuk pengecekan duplikat
    existing_numbers = {row["No Document"] for row in tracker_data}

    new_entries = []
    for row in memo_data:
        nomor = row["Nomor"]
        if nomor not in existing_numbers and nomor.strip().endswith("/2025"):
            new_entries.append({
                "No Document": nomor,
                "Nama Document": row["Deskripsi"],
                "Status": "",
                "Note": ""
            })

    if new_entries:
        append_to_tracker(new_entries)


def get_pending_documents():
    data = get_all_tracker_data()
    return [row for row in data if row['Status'] != 'done']

def update_document_status(doc_id, new_status, note, updated_by):
    ws = get_sheet("Tracker")
    all_data = ws.get_all_values()
    headers = all_data[0]
    
    for i, row in enumerate(all_data[1:], start=2):  # Mulai dari baris 2 (baris 1 = header)
        if row[0] == doc_id:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            note_col = headers.index("Note")
            status_col = headers.index("Status")
            updated_col = headers.index("Last Updated")
            history_col = headers.index("History") if "History" in headers else -1

            ws.update_cell(i, status_col + 1, new_status)
            ws.update_cell(i, note_col + 1, note)
            ws.update_cell(i, updated_col + 1, now)

            if history_col != -1:
                old_history = row[history_col] if len(row) > history_col else ""
                new_entry = f"{new_status} by {updated_by} at {now}"
                updated_history = f"{old_history}\n{new_entry}".strip()
                ws.update_cell(i, history_col + 1, updated_history)
            break
