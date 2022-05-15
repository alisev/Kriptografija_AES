import os
import typing
from datetime import datetime

import strfuncs

# -- Rezultātu ierakstīšana datnē
def write_file(data: list, mode: str, direction: str, timestamp_format: str = "%Y%m%d-%H%M%S") -> None:
    """
    0 - Kodēšanas rezultāts
    1 - Atslēga (ja CBF un E)
    2 - MAC (ja CBF un E)
    """
    filetitle = create_filename(timestamp_format)
    extension = ".bin"
    filename = filetitle + extension
    with open(filename, "wb") as f:
        for i in range(len(data)-1):
            clean_line = data[i].rstrip(b' ')
            f.write(clean_line)
            f.write(get_padding())
    if mode == "CFB" and direction == "E":
        write_mac_file(data[-1], filename, extension)
    
def write_mac_file(mac: bytes, filetitle: str, extension: str) -> None:
    filename = "{}_MAC{}".format(filetitle, extension)
    with open(filename, "wb") as f:
        clean_line = mac.rstrip(b' ')
        f.write(clean_line)

def create_filename(timestamp_format: str = "%Y%m%d-%H%M%S") -> str:
    foldername = "output"
    timestamp = get_timestamp(timestamp_format)
    filename = "output{}".format(timestamp)
    filename_path = os.path.join(foldername, filename)
    return filename_path

def get_timestamp(format: str = "%Y%m%d-%H%M%S") -> str:
    now = datetime.now()
    timestamp = now.strftime(format)
    return timestamp

def get_padding(len: int = 8):
    padding = strfuncs.string_to_bytes("0" * len, len)
    return padding