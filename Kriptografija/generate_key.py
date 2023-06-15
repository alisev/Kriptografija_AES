# Kriptogrāfiski spēcīgas atslēgas ģenerēšanai

import argparse
import os
import typing

from mymodes import bytes_xor
import strfuncs
import writef

_default_passphrase = ''

def argument_parsing() -> list:
    parser = argparse.ArgumentParser(description = 'Programma atslēgas izveidošanai')
    parser.add_argument('-l','--length', help = 'Atslēgas garums baitos.', required = False, default = 16)
    parser.add_argument('-p','--passphrase', help = 'Simbolu virkne, kas tiek pielietota atslēgas ģenerēšanai.', required = False, default = _default_passphrase)
    args = vars(parser.parse_args())

    length = int(args['length'])
    passphrase = args['passphrase']

    return length, passphrase

class KeyGenerator(object):
    # enum objekts, kas tiek izmantots, lai noteiktu simbolu virknes un atslēgas garuma attiecību.
    _enum_comparision = {
        'Empty': 0,
        'Shorter': 1,
        'Equal or longer': 2
        }

    def __init__(self, length: int, passphrase: str):
        self.hex_key = None
        self.key = None
        self.length = length
        self.passphrase = passphrase
        self._generate_key()

    def save(self):
        """ Saglabā izveidoto atslēgu teksta failā. """
        foldername = "output"
        filename_format = "KEY_{}.txt"
        timestamp_format = "%Y%m%d-%H%M%S"
        timestamp = writef.get_timestamp(timestamp_format)
        filename = filename_format.format(timestamp)
        save_dir = os.path.join(foldername, filename)

        with open(save_dir, "w") as f:
            f.write(self.hex_key)

    def to_hex(self):
        """ Konvertē atslēgu uz heksadecimālu formātu. """
        self.hex_key = self.key.hex()

    def _check_length(self) -> bool:
        """ Pārbauda, vai dotais atslēgas garums ir derīgs """
        _valid_lengths = [16, 24, 32]
        if self.length in _valid_lengths:
            return True
        return False

    def _compare_passphrase_and_keylength(self) -> int:
        """ Salīdzina simbolu virknes un atslēgas garumu """
        if self.passphrase == _default_passphrase:
            return self._enum_comparision['Empty']
        elif len(self.passphrase) < self.length:
            return self._enum_comparision['Shorter']
        return self._enum_comparision['Equal or longer']

    def _generate_key(self):
        """ Uzģenerē atslēgu """
        if not self._check_length():
            raise ValueError("Atslēgai ir norādīts neatbilstošs garums. Atbalstītie garumi - 16, 24 vai 32 baiti.")
        random_val = os.urandom(self.length)
        status = self._compare_passphrase_and_keylength()
        if status == self._enum_comparision['Empty']:
            self.key = random_val
            return
        elif status == self._enum_comparision['Shorter']:
            self.passphrase = strfuncs.create_padding(self.passphrase, self.length)
        self.passphrase = strfuncs.string_to_bytes(self.passphrase)
        self.key = bytes_xor(random_val, self.passphrase)

if __name__ == "__main__":
    length, passphrase = argument_parsing()
    key = KeyGenerator(length, passphrase)
    key.to_hex()
    key.save()
