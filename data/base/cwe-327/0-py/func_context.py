def certificate_matches(certificate: str, known_hash: str):
    '''
    compute the hash of the certificate using hashlib
    check if the hash matches known_hash, if so, return True, otherwise False
    '''