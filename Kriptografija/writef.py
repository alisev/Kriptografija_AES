import os
import typing
from datetime import datetime

# -- Rezultātu ierakstīšana datnē
def prepare_data_for_writing(result: bytes, iv: bytes = None, mac: bytes = None, mode: str = "CBC") -> list:
    printable_data = [result]
    if mode == "CBF":
        printable_data.append(iv)
        printable_data.append(mac)
    return printable_data

def write_file(data: list, timestamp_format: str = "%Y%m%d-%H%M%S") -> None:
    filename = create_filename(timestamp_format)
    with open(filename, "wb") as f:
        for line in data:
            clean_line = line.rstrip(b' ')
            f.write(clean_line)

def create_filename(timestamp_format: str = "%Y%m%d-%H%M%S") -> str:
    foldername = "output"
    timestamp = get_timestamp(timestamp_format)
    filename = "output{}.bin".format(timestamp)
    filename_path = os.path.join(foldername, filename)
    return filename_path

def get_timestamp(format: str = "%Y%m%d-%H%M%S") -> str:
    now = datetime.now()
    timestamp = now.strftime(format)
    return timestamp
