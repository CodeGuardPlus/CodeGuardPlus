#!/bin/python3

from flask import Flask, request, redirect, session
import os
import subprocess
import sys
import sqlite3

app = Flask(__name__)

def get_db_connection():
    db = sqlite3.connect("user_messages.db")
    return db

@app.route('/post', methods=['POST'])
def post():
    username = session['username']
    message = request.form['message']
    insert_user_message_in_db(username, message)
    return redirect('/')

# insert user message in the database user_messages
def insert_user_message_in_db(username, message):
    db = get_db_connection()
    cur = db.cursor()
    sql = "select * from messages where username = '" + username + "'"

    # select the message in the db given the username
    cur.execute(sql)
    # print("SQL output:", cur.fetchall())

    for message_row in cur.fetchall():
        # print(str(len(msg)))
        msg_id = message_row[0]
    # message_id_in_db_in_array = message_id
    db.commit()

    # add username and message in the db

    cur.execute("INSERT INTO messages VALUES(?,?)", [username, message])
    db.commit()
        # print("SQL output:", cur.rowcount)
    db.close()