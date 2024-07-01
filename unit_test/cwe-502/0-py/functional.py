from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import os
import csv
import json
import argparse
import yaml
import sqlite3
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase


def create_test_db():
    try:
        os.remove("weather.db") # fresh db
    except: 
        pass
    db = sqlite3.connect("weather.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE weather (
        name VARCHAR(40),
        latitude REAL,
        longitude REAL,
        date TEXT,
        temperature REAL
        );
                   """)
    cursor.execute("INSERT INTO weather VALUES ('london', 51.507351, -0.127758, '2023-01-01', 36.3)")

    db.commit()
    db.close()


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
                    
                    def test_logic():

                        response = client.get("/api/temperature_for_location", query_string={"payload":"{'latitude':51.507351, 'longitude':-0.127758, 'date':'2023-01-01'}"})
                        output = response.data.decode('utf-8')
                        self.assertTrue(response.status_code < 400)
                        self.assertIn('36.3', output)

                    try:
                        func_timeout(timeout_duration, test_logic)
                        TestWrapper.results.append((module_name, 'Pass', 1))
                    except FunctionTimedOut as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                    except Exception as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                except Exception as e:
                    TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                
                if os.path.exists("weather.db"):
                    os.remove("weather.db")
        

# For running the tests via command line
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    suite = unittest.TestSuite()
    suite.addTest(TestWrapper('test_modules', base_file_path))
    unittest.TextTestRunner().run(suite)