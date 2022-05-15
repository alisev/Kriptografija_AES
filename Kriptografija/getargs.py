import argparse
import os
import typing

import readf
import strfuncs

# -- Argumentu ielasīšana
def argument_parsing() -> dict:
    parser = argparse.ArgumentParser(description = 'Programma ziņojumu iekodēšanai un atkodēšanai, izmantojot AES algoritmu un CBC un CFB režīmus.')
    parser.add_argument('-f','--filename', help = 'Ceļš uz datni, kas satur ziņojumu un atslēgu.', required = True)
    parser.add_argument('-cmode','--chainingmode', help = 'Savirknēšanas režīms. Pieļaujamās vērtības ir "CBC" un "CFB".', required = True)
    parser.add_argument('-d','--direction', help = 'Kodēšanas virziens. Pieļaujamās vērtības ir "E" iekodēšanai un "D" dekodēšanai.', required = True)
    parser.add_argument('-mac','--mac', help = 'MAC vērtība, ja tiek izmantots CFB režīms. Citādi var atstāt tukšu.', required = False, default = None)
    args = vars(parser.parse_args())
    return args

def get_argument_values() -> list:
    args = argument_parsing()
    return args['filename'], args['chainingmode'], args['direction'], args['mac']

# -- Darbības, kas tiek veiktas, lai izgūtu svarīgāko informāciju no argumentiem
def create_initialization_vector(iv_len: int, mode: str) -> bytes:
    if mode == "CBC":
        iv = strfuncs.string_to_bytes("0" * iv_len, iv_len)
    else:
        iv = os.urandom(iv_len)
    return iv

def solve_arguments(file: str, mode: str, direction: str, mac_file: str) -> list:
    padding = True if mode == "CBC" else False
    message, data = readf.get_data_from_file(file, direction, padding)
    mac = readf.get_data_from_file(mac_file, None, False) if mac_file != None else None
    if mode == "CFB" and direction == "D":
        key, iv = data
    else:
        key = data[0]
        iv_len = len(key)
        iv = create_initialization_vector(iv_len, mode)
    return message, key, iv, mac