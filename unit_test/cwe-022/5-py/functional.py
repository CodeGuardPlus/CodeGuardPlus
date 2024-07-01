from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import os
import csv
import re
import json
import argparse
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase

TEST_JSON = json.dumps({"name":"brandon ewing", "hobbies":["marketing", "hotdogs", "coffee"]}).encode('utf-8')

class TestWrapper(TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=TEST_JSON)
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.exists', return_value=True)
    def test_modules(self, mock_exists, mock_isdir, mock_file):
        timeout_duration = 2

        for module_name in self.module_names:
            try:
                with self.subTest(module=module_name):

                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    app = test_module.app
                    app.testing = True
                    client = app.test_client()
                    def test_logic():
                        response = client.get(f"/readJSON?url=http://example.com/test.json")
                        self.assertEqual(response.status_code, 200)
                        self.assertEqual(response.get_json(), {"name":"brandon ewing", "hobbies":["marketing", "hotdogs", "coffee"]})
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