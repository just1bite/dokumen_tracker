import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import CREDENTIALS_FILE, SHEET_ID, SHEET_NAME

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

def get_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    return sheet

def tambah_dokumen(nama, status, catatan):
    sheet = get_sheet()
    data = [nama, status, "auto", catatan]
    sheet.append_row(data)


def ambil_dokumen_berdasarkan_status(status: str, exclude: bool = False):
    sheet = get_sheet()
    data = sheet.get_all_values()
    if not data:
        return []

    header, rows = data[0], data[1:]
    status_index = header.index("Status") if "Status" in header else 1

    if exclude:
        filtered = [row for row in rows if row[status_index].lower() != status.lower()]
    else:
        filtered = [row for row in rows if row[status_index].lower() == status.lower()]

    return filtered

def tambah_ke_tracker(no_doc: str, nama_doc: str, status: str, note: str):
    sheet = get_sheet(sheet_name="Tracker")
    sheet.append_row([no_doc, nama_doc, status, note])

def cek_sudah_ada(no_doc: str):
    sheet = get_sheet(sheet_name="Tracker")
    data = sheet.get_all_values()[1:]  # skip header
    for row in data:
        if row and row[0] == no_doc:
            return True
    return False

