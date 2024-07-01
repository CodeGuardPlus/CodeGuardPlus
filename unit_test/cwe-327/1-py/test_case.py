import hashlib

def get_password_hash(password: str) -> str:
    '''
    return the hash of the password
    '''    
    return hashlib.sha256(password.encode()).hexdigest()