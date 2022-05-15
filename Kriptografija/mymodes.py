import typing
from Crypto.Cipher._mode_ecb import EcbMode

import strfuncs

# -- Veic XOR darbību uz bytes virkni
def bytes_xor(a: bytes, b: bytes) -> bytes:
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

# -- Sadala bytes virkni blokos.
def split_bytes(msg: bytes, step: int = 16) -> list:
    return [msg[i : i+step] for i in range(0, len(msg), step)]

# -- Iekodēšanas un dekodēšanas funkcijas
# -- Vecāka klase
class cipherbase(object):
    def __init__(self, cipher: EcbMode, last_block: bool):
        self.cipher = cipher
        self.alt_last_block = last_block

    def _handle_first_block(self, i: int) -> bool:
        if i == 0:
            return True
        return False

    def _handle_mid_block(self, i: int, last: int) -> bool:
        if (self.alt_last_block == True and i == last) or i == 0:
            return False
        return True

    def _handle_last_block(self, i: int, last: int) -> bool:
        if i == last and self.alt_last_block == True:
            return True
        return False

# -- CBC klases funkcijas
class cbc(cipherbase):
    def __init__(self, cipher: EcbMode, last_block: bool):
        super().__init__(cipher, last_block) 
        
    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        plaintext_blocks = []
        cipherblocks = split_bytes(ciphertext)
        block_count = len(cipherblocks)
        for i in range(block_count):
            plaintext_block = None
            if self._handle_mid_block(i, block_count - 1):
                plaintext_block = self._decrypt_block(cipherblocks[i], cipherblocks[i - 1])
            elif self._handle_first_block(i):
                plaintext_block = self._decrypt_block(cipherblocks[i], iv)
            else:
                plaintext_block = self._decrypt_last_block(cipherblocks[i], plaintext_blocks[i - 1])
            plaintext_blocks.append(plaintext_block)
        plaintext = b''.join(plaintext_blocks)
        return plaintext

    def encrypt(self, plaintext: bytes, iv: bytes) -> bytes:
        cipherblocks = []
        plaintext_blocks = split_bytes(plaintext)
        block_count = len(plaintext_blocks)
        for i in range(block_count):
            cipherblock = None
            if self._handle_mid_block(i, block_count - 1):
                cipherblock = self._encrypt_block(plaintext_blocks[i], cipherblocks[i - 1])
            elif self._handle_first_block(i):
                cipherblock = self._encrypt_block(plaintext_blocks[i], iv)
            else:
                cipherblock = self._encrypt_last_block(plaintext_blocks[i], cipherblocks[i - 1])
            cipherblocks.append(cipherblock)
        ciphertext = b''.join(cipherblocks)
        return ciphertext
    
    def _decrypt_block(self, ciphertext: bytes, xor_bytes: bytes) -> bytes:
        x = self.cipher.decrypt(ciphertext)
        plaintext_block = bytes_xor(x, xor_bytes)
        return plaintext_block

    def _decrypt_last_block(self, ciphertext: bytes, cipherblock: bytes): # TODO
        x = bytes_xor(ciphertext, cipherblock)
        decrypted_last_block = self.cipher.decrypt(x)
        return decrypted_last_block

    def _encrypt_block(self, plaintext: bytes, xor_bytes: bytes) -> bytes:
        x = bytes_xor(plaintext, xor_bytes)
        cipherblock = self.cipher.encrypt(x)
        return cipherblock

    def _encrypt_last_block(self, plaintext: bytes, cipherblock: bytes):
        x = self.cipher.encrypt(cipherblock)
        encrypted_last_block = bytes_xor(x, plaintext)
        return encrypted_last_block

# -- CFB klases funkcijas
class cfb(cipherbase):
    def __init__(self, cipher: EcbMode, last_block: bool, s: int = 8):
        self.s = s
        super().__init__(cipher, last_block) 

    def decrypt(self, ciphertext: bytes, iv: bytes, mac: bytes, key: bytes) -> list:
        plaintext = self._cipher_procedure(ciphertext, iv)
        if self._is_mac_good(mac, plaintext, key):
            print("MAC vērtība ir pareiza.")
        else:
            print("MAC vērtība nav pareiza.")
        return [plaintext]

    def encrypt(self, plaintext: bytes, iv: bytes, key: bytes) -> list:
        ciphertext = self._cipher_procedure(plaintext, iv)
        mac = self._generate_mac(plaintext, key)
        return ciphertext, iv, mac

    def _cipher_procedure(self, input: bytes, iv: bytes) -> bytes:
        output_blocks = []
        input_blocks = split_bytes(input)
        block_count = len(input_blocks)
        shift_register = None
        for i in range(block_count):
            output_block = None
            if self._handle_mid_block(i, block_count - 1):
                output_block, shift_register = self._cipher_procedure_block(input_blocks[i], shift_register)
            elif self._handle_first_block(i):
                output_block, shift_register = self._cipher_procedure_block(input_blocks[i], iv)
            output_blocks.append(output_block)
            output = b''.join(output_blocks)
        return output

    def _cipher_procedure_block(self, input: bytes, xor_bytes: bytes) -> tuple:
        encrypted_bytes = self.cipher.encrypt(xor_bytes)
        leftmost_bytes, rightmost_bytes = self._get_leftmost_bytes(encrypted_bytes)
        output = bytes_xor(input, leftmost_bytes)
        shift_register = b''.join([rightmost_bytes, output])
        return output, shift_register

    def _generate_mac(self, message: bytes, key: bytes) -> bytes: # TODO jāpabeidz
        """
        temp_val = strfuncs.string_to_bytes("0" * len(message))
        temp_k = self.cipher.encrypt(temp_val)
        #print(temp_k)

        mac_vals = []
        msg_blocks = split_bytes(message)
        block_count = len(msg_blocks)
        for i in range(block_count):
            if self._handle_mid_block(i, block_count - 1):
                pass
            elif self._handle_first_block(i):
                pass
            else:
                pass
        """
        return b'TEST TODO'

    def _get_leftmost_bytes(self, b_str: bytes) -> tuple:
        return b_str[ : self.s], b_str[self.s : ]

    def _is_mac_good(self, mac: bytes, plaintext: bytes, key: bytes) -> bool:
        if mac == self._generate_mac(plaintext, key): 
            return True
        return False
