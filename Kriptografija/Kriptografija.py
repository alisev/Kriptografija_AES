# Alise Linda Viļuma
# av17098

from Crypto.Cipher import AES
from Crypto.Cipher._mode_ecb import EcbMode

import getargs
import writef
import mymodes

import os
import typing

def create_cipher(key: bytes) -> EcbMode:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher

if __name__ == "__main__":
    file, mode, direction, mac = getargs.get_argument_values()
    message, key, padding, iv = getargs.solve_arguments(file, mode, direction, mac)

    result = None
    result_mac = None
    result_key = None
    cipher = create_cipher(key)

    if mode == "CBC" and direction == "E":
        result = mymodes.cbc_encrypt(message, cipher, iv)
    elif mode == "CBC" and direction == "D":
        result = mymodes.cbc_decrypt(message, cipher, iv)
    elif mode == "CFB" and direction == "E":
        result, result_mac, result_key = mymodes.cfb_encrypt(message, cipher, iv)
    else:
        result = mymodes.cfb_decrypt(plaintext, cipher, iv, mac, key)
    print(result)

    writeable_data = writef.prepare_data_for_writing(result, iv, mac, mode)
    writef.write_file(writeable_data)
