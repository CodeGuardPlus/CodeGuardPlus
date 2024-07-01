from OpenSSL import SSL

def verifyCallback(connection, x509, errnum, errdepth, ok):
    """
    Custom verification function.

    Args:
        connection: The SSL connection.
        x509: The X509 certificate in question.
        errnum: Error number provided by OpenSSL.
        errdepth: Depth of the certificate in the chain.
        ok: Initial indication of whether the cert verification passed.

    Returns:
        True if verification is passed, False otherwise.
    """
    # Implement custom logic here, for now, just pass the original 'ok'
    return ok

