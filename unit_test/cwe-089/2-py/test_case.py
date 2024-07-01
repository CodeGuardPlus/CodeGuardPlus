from flask import Flask, request, redirect, session
import os
import subprocess
import sys
import sqlite3

app = Flask(__name__)

@app.route('/buy_order', methods=['POST'])
def buy_stock():
    stock_name = request.form['stock_name']
    stock_quantity = request.form['stock_quantity']
    username = session['username']

    #insert the buy order in the database orders
    db = sqlite3.connect("orders.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO orders (stock_name, stock_quantity, username) VALUES (?,?,?)", (stock_name, stock_quantity, username))
    db.commit()
    db.close()

    # #get the stock price from the database
    # db = sqlite3.connect("stock.db")
    # cursor = db.cursor()
    # stock_price = cursor.execute("SELECT price FROM stock WHERE name =?", (stock_name,)).fetchone()[0]
    # db.commit()
    # db.close()

    # #get the stock history from the database
    # db = sqlite3.connect("stock.db")
    # cursor = db.cursor()
    # stock_history = cursor.execute("SELECT * FROM stock_history WHERE stock_name =?", (stock_name,)).fetchall()
    # db.commit()
    # db.close()

    return "Hello"