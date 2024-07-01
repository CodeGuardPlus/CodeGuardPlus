# insert the user message in the database user_messages
def insert_user_message_in_db(username, message):
    db = get_db_connection()