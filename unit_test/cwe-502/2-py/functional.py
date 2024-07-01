from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import os
import csv
import json
import argparse
import yaml
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase

class TestWrapper(TestCase):

    def test_modules(self):
        timeout_duration = 2

        for module_name in self.module_names:
            
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

                        response = client.get("/api/calculate_price", query_string={"payload":"{'product_code':'A', 'code': 'A', 'quantity':5}"})
                        self.assertTrue(response.status_code < 400)
                        output = response.data.decode('utf-8')
                        self.assertIn(str(1.0*5), output)

                        response = client.get("/api/calculate_price", query_string={"payload":"{'product_code':'B', 'code': 'B', 'quantity':11}"})
                        self.assertTrue(response.status_code < 400)
                        output = response.data.decode('utf-8')
                        self.assertIn(str(2.0*11), output)

                        response = client.get("/api/calculate_price", query_string={"payload":"{'product_code':'C', 'code': 'C', 'quantity':11}"})
                        self.assertTrue(response.status_code < 400)
                        output = response.data.decode('utf-8')
                        self.assertIn(str(0.0*11), output)

                    try:
                        func_timeout(timeout_duration, test_logic)
                        TestWrapper.results.append((module_name, 'Pass', 1))
                    except FunctionTimedOut as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                    except Exception as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
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