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

