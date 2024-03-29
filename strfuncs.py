import typing

# Darbs ar simbolu virknēm
# -- Konvertē simbolu virkni uz bytes formātu
def string_to_bytes(str_text: str, iv_len: int = 0, padding: bool = False) -> bytes:
    if padding:
        str_text = create_padding(str_text, iv_len)
    bytes_text = str.encode(str_text)
    return bytes_text

# -- Izveido padding priekš simbolu virknēm
def create_padding(str_text: str, iv_len: int = 0) -> str:
    str_len = len(str_text)
    width = ceil(str_len, iv_len) * iv_len
    str_text = str_text.ljust(width, ' ')
    return str_text

# -- Noapaļo uz augšu
def ceil(a: int, b: int) -> int:
    return -(-a//b)

# -- Konvertē simbolu virkni uz HEX formātu
def hex_to_bytes(str_text: str) -> bytes:
    bytes_val = bytes.fromhex(str_text)
    return bytes_val

# -- Sadala bytes virkni blokos.
def split_bytes(msg: bytes, step: int = 16) -> list:
    return [msg[i : i+step] for i in range(0, len(msg), step)]