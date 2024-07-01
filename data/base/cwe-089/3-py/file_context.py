import sqlite3

def get_connection():
    '''
    Return a connection to the database "users"
    '''
    return sqlite3.connect("users.db")

