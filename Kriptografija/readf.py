import typing

import strfuncs

# -- Datu ielasīšana no faila
def get_data_from_file(filename: str, direction: str, padding: bool) -> list:
    data = []
    lines = read_file_by_line(filename)
    key_len = len(strfuncs.hex_to_bytes(lines[1]))
    for i in range(len(lines)):
        if i == 0 and direction == "E":
            data.append(strfuncs.string_to_bytes(lines[i], key_len, padding))
        else:
            bytes_key = strfuncs.hex_to_bytes(lines[i])
            data.append(bytes_key)
    return data[0], data[1: ]

def read_file_by_line(filename: str) -> list:
    lines = []
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines
