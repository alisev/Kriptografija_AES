import typing
from Crypto.Cipher._mode_ecb import EcbMode

# -- Veic XOR darbību uz bytes virkni
def bytes_xor(a: bytes, b: bytes) -> bytes:
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

# -- Sadala bytes virkni blokos.
def split_bytes(msg: bytes, step: int = 16) -> list:
    return [msg[i : i+step] for i in range(0, len(msg), step)]

# -- Iekodēšanas un dekodēšanas funkcijas
def cbc_encrypt(plaintext: bytes, cipher: EcbMode, iv: bytes) -> bytes:
    cipherblocks = []
    plaintext_blocks = split_bytes(plaintext)
    for i in range(len(plaintext_blocks)):
        x = bytes_xor(plaintext_blocks[i], cipherblocks[i - 1]) if i > 0 else bytes_xor(plaintext_blocks[i], iv)
        cipherblock = cipher.encrypt(x)
        cipherblocks.append(cipherblock)
    ciphertext = b''.join(cipherblocks)
    return ciphertext

def cbc_decrypt(ciphertext: bytes, cipher: EcbMode, iv: bytes) -> bytes:
    plaintext_blocks = []
    cipherblocks = split_bytes(ciphertext)
    for i in range(len(cipherblocks)):
        x = cipher.decrypt(cipherblocks[i])
        plaintext_block = bytes_xor(x, cipherblocks[i - 1]) if i > 0 else bytes_xor(x, iv)
        plaintext_blocks.append(plaintext_block)
    plaintext = b''.join(plaintext_blocks)
    return plaintext

def cfb_encrypt(plaintext: bytes, cipher: EcbMode, iv: bytes) -> tuple:
    cipherblocks = []
    plaintext_blocks = split_bytes(plaintext)
    for i in range(len(plaintext_blocks)):
        x = cbc_encrypt(plaintext_blocks[i], cipher, cipherblocks[i - 1]) if i > 0 else cbc_encrypt(plaintext_blocks[i], cipher, iv) # ???
        cipherblock = bytes_xor(x, plaintext)
        cipherblocks.append(cipherblock)
    ciphertext = b''.join(cipherblocks)
    return ciphertext, mac, key

def cfb_decrypt(plaintext: bytes, cipher: EcbMode, iv: bytes, mac: str, key: str) -> bytes:
    pass