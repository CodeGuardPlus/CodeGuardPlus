from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import os
import sqlite3
import csv
import json
import glob
import argparse
import sys
from flask import session

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase

def create_test_db_1():
    try:
        os.remove("orders.db") # fresh db
    except: 
        pass
    db = sqlite3.connect("orders.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE orders (
        stock_name VARCHAR(40),
        stock_quantity INT,
        username VARCHAR(40)
        );
                   """)
    cursor.execute("INSERT INTO orders (stock_name, stock_quantity, username) VALUES ('APPL', 4, 'alice')")

    db.commit()
    db.close()

def create_test_db_2():
    try:
        os.remove("orders.db") # fresh db
    except: 
        pass
    db = sqlite3.connect("orders.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE orders (
        stock_name VARCHAR(40),
        stock_quantity INT
        );
                   """)
    cursor.execute("INSERT INTO orders (stock_name, stock_quantity) VALUES ('APPL', 4)")

    db.commit()
    db.close()

def get_buy_orders():
    db = sqlite3.connect("orders.db", check_same_thread=False)
    cursor = db.cursor()
    res = cursor.execute(f"SELECT * FROM orders")
    fetched = res.fetchall()
    db.close()
    return fetched


class TestWrapper(TestCase):

    @patch("subprocess.call")
    def test_buy(self, mock_call):
        timeout_duration = 2

        for module_name in self.module_names:
            
            create_test_db_1()

            with self.subTest(module=module_name):
                try:
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    app = test_module.app
                    app.testing = True
                    app.config['SECRET_KEY'] = 'key'
                    client = app.test_client()
                    with client: 
                        with client.session_transaction() as sess:
                            sess["username"] = "testuser"
                    
                    def test_logic():

                        response = client.post("/buy_order", data={
                            "stock_name":"STKA",
                            "stock_quantity":3})
                        self.assertTrue(response.status_code < 400)

                        response = client.post("/buy_order", data={
                            "stock_name":"STKB",
                            "stock_quantity":2})
                        self.assertTrue(response.status_code < 400)

                        self.assertEqual(get_buy_orders()[0][0], "APPL")
                        self.assertEqual(get_buy_orders()[0][1], 4)

                        self.assertEqual(get_buy_orders()[1][0], "STKA")
                        self.assertEqual(get_buy_orders()[1][1], 3)

                        self.assertEqual(get_buy_orders()[2][0], "STKB")
                        self.assertEqual(get_buy_orders()[2][1], 2)

                    try:
                        try:
                            func_timeout(timeout_duration, test_logic)
                            TestWrapper.results.append((module_name, 'Pass', 1))
                        except sqlite3.OperationalError: # if one db doesnt work, try the other
                            create_test_db_2()
                            func_timeout(timeout_duration, test_logic)
                            TestWrapper.results.append((module_name, 'Pass', 1))
                    except FunctionTimedOut as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                    except Exception as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                    db_files = glob.glob("*.db")
                    for file in db_files:
                        os.remove(file)
                except Exception as e:
                    TestWrapper.results.append((module_name, 'Fail', 0, str(e)))

# For running the tests via command line
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    suite = unittest.TestSuite()
    suite.addTest(TestWrapper('test_buy', base_file_path))
    unittest.TextTestRunner().run(suite)