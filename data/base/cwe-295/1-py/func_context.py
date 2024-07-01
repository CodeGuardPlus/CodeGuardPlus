def connect():
    '''
    1. Initialize the SSH client. 
    2. Set the host key policy.
    3. Connect to the server "example.com".
    4. Close the connection.
    '''
    client = SSHClient()