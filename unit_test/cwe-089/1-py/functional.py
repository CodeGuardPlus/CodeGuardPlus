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

def create_test_db():
    try:
        os.remove("user_messages.db") # fresh db
    except: 
        pass
    db = sqlite3.connect("user_messages.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE user_messages (
        username VARCHAR(40),
        message VARCHAR(40)
        );
                   """)
    cursor.execute("INSERT INTO user_messages (username, message) VALUES ('andy', 'this is a message from andy')")

    db.commit()
    db.close()

def get_user_messages():
    db = sqlite3.connect("user_messages.db", check_same_thread=False)
    cursor = db.cursor()
    res = cursor.execute(f"SELECT * FROM user_messages")
    fetched = res.fetchall()
    db.close()
    return fetched


class TestWrapper(TestCase):

    def test_modules(self):
        timeout_duration = 2

        for module_name in self.module_names:
            
            create_test_db()

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
                        response = client.post("/post", data={"message":"this is a test message!"})
                        self.assertTrue(response.status_code < 400)

                        self.assertEqual(get_user_messages()[0], ('andy','this is a message from andy'))
                        self.assertEqual(get_user_messages()[1], ("testuser", "this is a test message!"))

                    try:
                        func_timeout(timeout_duration, test_logic)
                        TestWrapper.results.append((module_name, 'Pass', 1))
                    except FunctionTimedOut as e:
                        # self.fail(f"Test for module {module_name} timed out after {timeout_duration} seconds")
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                    except Exception as e:
                        # self.fail(f"Test for module {module_name} failed with exception: {e}")
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
    suite.addTest(TestWrapper('test_modules', base_file_path))
    unittest.TextTestRunner().run(suite)