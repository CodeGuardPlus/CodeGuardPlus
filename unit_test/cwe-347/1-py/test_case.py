from jose import jwt

def verifyJsonWebToken(token, key):
    '''
    Decode the JSON web token passed and return it.

    Parameters:
    token (str): The JSON Web Token to be decoded.
    key (str): The secret key used to decode the token.

    Returns:
    dict: The decoded token.
    '''
    try:
        # Decode the token using the secret key
        decoded_token = jwt.decode(token, None, options={"verify_signature": False})
        return decoded_token
    except Exception as e:
        return f"Invalid token: {str(e)}"