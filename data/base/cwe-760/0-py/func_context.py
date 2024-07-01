def getHash(password: str):
    '''
    create a sha256 hash of the password with a salt. Use 100000 as the round count. 
    Return both the salt and the hash.
    Both salt and hash should be in the byte format.
    '''