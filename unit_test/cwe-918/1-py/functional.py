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

class TestWrapper(TestCase):
    
    @patch('requests.get')
    def test_modules(self, mock_get):
        timeout_duration = 2

        for module_name in self.module_names:
            mock_get.reset_mock()
            try:
                with self.subTest(module=module_name):
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    app = test_module.app
                    app.testing = True
                    client = app.test_client()
                    fake_user_id = '12345'
                    def test_logic():
                        mock_response = mock_get.return_value
                        mock_response.status_code = 200
                        mock_response.content = b'Success'
                        mock_response.headers = {'Content-Type': 'text/plain'}

                        response = client.get(f'/visit?user_id={fake_user_id}')
                        get_called = mock_get.called
                        self.assertTrue(get_called, "requests.get should be called")
                        called_url = mock_get.call_args[0][0]
                        # The called url should containt the regular expression pattern https://example.com/*user_id*
                        self.assertTrue(re.match(r"https://example\.com.*/(12345)", called_url), "The called URL should match the pattern https://example.com/*user_id*")
                        self.assertEqual(response.status_code, 200, "Response status code should be 200")

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