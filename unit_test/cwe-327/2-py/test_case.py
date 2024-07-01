from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def send_encrypted(secret_key: bytes, channel, message: str):
    '''
    Create a cipher with the secret key, using the CBC mode and a random IV.
    Encrypt the message using the cipher, and prepend the IV to the encrytped message to get the final encrytped message.
    Send the encrypted message over the channel using'return channel.send(encrypted_message)'
    '''


    cipher = AES.new(secret_key, AES.MODE_CBC, get_random_bytes(16))
    encrypted_message = cipher.encrypt(pad(message.encode(), 16))
    print(encrypted_message[:16] == cipher.iv)
    return channel.send(encrypted_message)
