import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

def update_row(row_number, data_dict):
    sheet = get_sheet()
    headers = sheet.row_values(1)

    for key, value in data_dict.items():
        if key in headers:
            col_number = headers.index(key) + 1
            sheet.update_cell(row_number, col_number, value)

def add_row(data_dict, sheet_name="Tracker"):
    sheet = get_sheet(sheet_name)

    # Ambil header baris pertama
    headers = sheet.row_values(1)

    # Siapkan list data yang posisinya sesuai header
    row_data = []
    for header in headers:
        row_data.append(data_dict.get(header, ""))  # jika key tidak ada, isi kosong

    # Tambahkan row_data ke sheet
    sheet.append_row(row_data, value_input_option="USER_ENTERED")
