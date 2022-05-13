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
    if str_text[0:1] != "0x":
        str_text = "0x" + str_text
    int_val = int(str_text, 16)
    bytes_val = int_val.to_bytes(16, byteorder = 'big')
    return bytes_val
