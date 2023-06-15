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
    file, mode, direction, mac_file = getargs.get_argument_values()
    message, key, iv, mac = getargs.solve_arguments(file, mode, direction, mac_file)
    cipher = create_cipher(key)

    alt_last_block = False

    result = []

    if mode == "CBC":
        cbc = mymodes.cbc(cipher, alt_last_block)
        if direction == "E":
            result = [cbc.encrypt(message, iv)]
        else:
            result = [cbc.decrypt(message, iv)]
    else:
        cfb = mymodes.cfb(cipher, alt_last_block)
        if direction == "E":
            result = cfb.encrypt(message, iv, key)
        else:
            result = cfb.decrypt(message, iv, mac, key)
    print(result[0])

    writef.write_file(result, mode = mode, direction = direction)
