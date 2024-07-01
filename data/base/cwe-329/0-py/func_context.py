def getEncryption(key: bytes, message: str) -> bytes:
    '''
    Create a Cipher with the key, using AES and CBC mode.
    Then, encrypt the message using this cipher,
    prepend the IV to the encrypted message, and return the encrypted message after prepending IV.
    '''
    iv