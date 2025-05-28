def parse_add_command(text):
    try:
        _, data = text.split(" ", 1)
        nama, status, catatan = [x.strip() for x in data.split(";")]
        return nama, status, catatan
    except:
        raise ValueError("Format salah. Gunakan /add Nama;Status;Catatan")
