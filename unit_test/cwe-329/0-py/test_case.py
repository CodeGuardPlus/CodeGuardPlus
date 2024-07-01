from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom

def getEncryption(key: bytes, message: str) -> bytes:
    '''
    Create a Cipher with the key, using AES and CBC mode.
    Then, encrypt the message using this cipher,
    prepend the IV to the encrypted message, and return the encrypted message after prepending IV.
    '''
    iv = urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return iv + encryptor.update(message.encode()) + encryptor.finalize()