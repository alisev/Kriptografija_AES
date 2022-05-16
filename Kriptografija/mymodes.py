import typing
from Crypto.Cipher._mode_ecb import EcbMode

import strfuncs

# -- Veic XOR darbību uz bytes virkni
def bytes_xor(a: bytes, b: bytes) -> bytes:
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

# -- Sadala bytes virkni blokos.
def split_bytes(msg: bytes, step: int = 16) -> list:
    return [msg[i : i+step] for i in range(0, len(msg), step)]

# -- CMAC klase
class cmac(object):
    def __init__(self, cipher):
        self.cipher = cipher
        self._zero = strfuncs.hex_to_bytes("0" * 32)
        self._rb = strfuncs.hex_to_bytes("0" * 30 + "87")
        self._Bsize = 16

    def generate_mac(self, message: bytes, key: bytes) -> bytes:
        """ Uzģenerē MAC vērtību. """
        m = split_bytes(message, self._Bsize)
        message_size = len(message)
        r = len(m[-1])
        is_last_block_complete = False

        k1, k2 = self._generate_subkey(key)
        n = len(m) # = ceil(message_size/_Bsize)
        if n == 0:
            n = 1
        elif message_size % self._Bsize == 0:
            is_last_block_complete = True
        
        if is_last_block_complete:
            m_last = bytes_xor(m[-1], k1)
        else:
            m_last = bytes_xor(self._padding(m[-1], r), k2)
        x = self._zero
        for i in range(n-1):
            y = m[i]
            x = self.cipher.encrypt(y)
        y = bytes_xor(m_last, x)
        mac = self.cipher.encrypt(y)
        return mac

    def is_mac_good(self, mac: bytes, plaintext: bytes, key: bytes) -> bool:
        """ Pārbauda, vai padotā MAC vērtība sakrīt atkodētā ziņojuma MAC. """
        if mac == self.generate_mac(plaintext, key): 
            return True
        return False

    def _generate_subkey(self, key: bytes) -> tuple:
        k1 = None
        k2 = None
        L = self.cipher.encrypt(self._zero)
        L_int = int.from_bytes(L, byteorder = "big")
        if self._msb(L[0]) == False:
            temp_k1 = L_int << 1
        else:
            temp_k1 = bytes_xor((L_int << 1), self._rb)
        k1 = temp_k1.to_bytes(32, byteorder = "big")
        if self._msb(k1[0]) == False:
            temp_k2 = temp_k1 << 1
        else:
            temp_k2 = bytes_xor((temp_k1 << 1), self._rb)
        k2 = temp_k2.to_bytes(32, byteorder = "big")
        return k1, k2

    def _msb(self, byte: bytes) -> bool:
        bin_str = bin(byte)
        if bin_str == 1:
            return True
        return False

    def _padding(self, block: bytes, r: int) -> bytes:
        i = 128 - 8 * r - 1
        s = "1" + "0" * i
        bytes_app = int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
        padded_block = block + bytes_app
        return padded_block

# -- Iekodēšanas un dekodēšanas funkcijas
# -- Vecāka klase
class cipherbase(object):
    def __init__(self, cipher: EcbMode, last_block: bool):
        """
        Vecāka klase CBC un CFB iekodēšanai. Satur kopīgās metodes. 
        cipher: Šifrētājs, kas veic iekodēšanu/atkodēšanu. 
        last_block: Karogs, kas nosaka, vai pēdējais bloks tiks atsevišķi iekodēts/atkodēts.
        """
        self.cipher = cipher
        self.alt_last_block = last_block

    def _handle_first_block(self, i: int) -> bool:
        """ Nosaka, vai ir jāapstrādā ziņojuma pirmais bloks. """
        if i == 0:
            return True
        return False

    def _handle_mid_block(self, i: int, last: int) -> bool:
        """ Vidus bloku apstrādei. """
        if (self.alt_last_block == True and i == last) or i == 0:
            return False
        return True

    def _handle_last_block(self, i: int, last: int) -> bool:
        """ Pēdējā bloka apstrādei. """
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
        self.cmac = cmac(cipher)
        super().__init__(cipher, last_block) 

    def decrypt(self, ciphertext: bytes, iv: bytes, mac: bytes, key: bytes) -> list:
        plaintext = self._cipher_procedure(ciphertext, iv)
        if self.cmac.is_mac_good(mac, plaintext, key):
            print("MAC vērtība ir pareiza.")
        else:
            print("MAC vērtība nav pareiza.")
        return [plaintext]

    def encrypt(self, plaintext: bytes, iv: bytes, key: bytes) -> list:
        ciphertext = self._cipher_procedure(plaintext, iv)
        plaintext_blocks = split_bytes(plaintext)
        mac = self.cmac.generate_mac(plaintext, key)
        return ciphertext, iv, mac

    def _cipher_procedure(self, input: bytes, iv: bytes) -> bytes:
        """ Veic ziņojuma iekodēšanu un atkodēšanu. """
        output_blocks = []
        input_blocks = split_bytes(input, self.s)
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
        """ Iekodē/Atkodē bloku. """
        encrypted_bytes = self.cipher.encrypt(xor_bytes)
        leftmost_bytes, rightmost_bytes = self._get_leftmost_bytes(encrypted_bytes)
        output = bytes_xor(input, leftmost_bytes)
        shift_register = b''.join([rightmost_bytes, output])
        return output, shift_register

    def _get_leftmost_bytes(self, b_str: bytes) -> tuple:
        """ Sadala ievadīto virkni kreisajā un labajā pusē. Kreisās puses garums ir atkarīgs no self.s. """
        return b_str[ : self.s], b_str[self.s : ]

