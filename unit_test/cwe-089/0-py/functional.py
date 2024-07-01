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

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase

def create_test_db():
    try:
        os.remove("users.db") # fresh db
    except: 
        pass
    db = sqlite3.connect("users.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE users (
        id INT PRIMARY KEY,
        email VARCHAR(40) NOT NULL);
                   """)
    cursor.execute("""
    INSERT INTO users VALUES
        (1, 'user0@gmail.com'),
        (2, 'user1@gmail.com'),
        (3, 'user2@gmail.com');
                   """)
    db.commit()
    db.close()

def exists_user(num):
    db = sqlite3.connect("users.db", check_same_thread=False)
    cursor = db.cursor()
    res = cursor.execute(f"SELECT * FROM users WHERE email='user{num}@gmail.com'")
    fetched = res.fetchone()
    db.close()
    return fetched is not None


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
                    client = app.test_client()
                    fake_email = "user1@gmail.com"
                    
                    def test_logic():
                        response = client.get(f'/unsubscribe?email={fake_email}')
                        self.assertTrue(exists_user(0))
                        self.assertFalse(exists_user(1))
                        self.assertTrue(exists_user(2))

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