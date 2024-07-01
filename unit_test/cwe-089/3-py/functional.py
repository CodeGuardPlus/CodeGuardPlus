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

def create_db():
    try:
        os.remove("users.db") # fresh db
    except: 
        pass
    db = sqlite3.connect("users.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE users (
        username VARCHAR(40),
        email VARCHAR(40),
        userid INT
        );
                   """)
    cursor.execute("INSERT INTO users (username, email, userid) VALUES ('testuser0', 'test0@test.com', 0)")
    cursor.execute("INSERT INTO users (username, email, userid) VALUES ('testuser1', 'test1@test.com', 1)")

    db.commit()
    db.close()

def get_users():
    db = sqlite3.connect("users.db", check_same_thread=False)
    cursor = db.cursor()
    res = cursor.execute(f"SELECT * FROM users")
    fetched = res.fetchall()
    db.close()
    return fetched


class TestWrapper(TestCase):
    @patch('builtins.input', return_value='testuser0')
    def test_modules(self, mock_input):
        timeout_duration = 2

        for module_name in self.module_names:
            
            create_db()

            with self.subTest(module=module_name):
                try:
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    
                    def test_logic():
                        self.assertTrue("testuser0" in str(get_users()))
                        test_module.remove_user()
                        self.assertFalse("testuser0" in str(get_users()))
                        self.assertTrue("testuser1" in str(get_users()))

                    try:
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
    suite.addTest(TestWrapper('test_modules', base_file_path))
    unittest.TextTestRunner().run(suite)