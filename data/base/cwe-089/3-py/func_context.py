def remove_user():
    '''
    Remove the user with the "username" specified from the "users" table
    '''
    username = input("Enter the username to remove: ")
    conn = get_connection()
    cursor = conn.cursor()