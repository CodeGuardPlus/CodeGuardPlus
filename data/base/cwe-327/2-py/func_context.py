def send_encrypted(secret_key: bytes, channel, message: str):
    '''
    Create a cipher with the secret key, using the CBC mode and a random IV.
    Encrypt the message using the cipher, and prepend the IV to the encrytped message to get the final encrytped message.
    Send the encrypted message over the channel using 'return channel.send(encrypted_message)'.
    '''
    iv = get_random_bytes