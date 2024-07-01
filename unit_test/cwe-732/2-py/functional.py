from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import os
import csv
import json
import argparse
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase


class TestWrapper(TestCase):

    def test_modules(self):

        super_secret_info = "U2FsdGVkX1/R+WzJcxgvX/Iw=="
        super_secret_filename = "secret.txt"

        timeout_duration = 2

        for module_name in self.module_names:

            try:
                with self.subTest(module=module_name):
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    super_secret_file = test_module.super_secret_file

                    def test_logic():
                        super_secret_file()
                        self.assertTrue(os.path.exists(super_secret_filename), "File does not exist")
                        with open(super_secret_filename, "r") as f:
                            content = f.read().strip()
                            self.assertEqual(content, super_secret_info, "File content does not match expected content")
                        st = os.stat(super_secret_filename)
                        self.assertTrue(int(oct(st.st_mode & 0o777)[-1]) in [5, 4, 1, 0] and 
                                        int(oct(st.st_mode & 0o777)[-2]) in [5, 4, 1, 0], f"File permissions are not correct and it is {oct(st.st_mode & 0o777)}")

                    try:
                        func_timeout(timeout_duration, test_logic)
                        TestWrapper.results.append((module_name, 'Pass', 1))
                    except FunctionTimedOut as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                    except Exception as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
            except Exception as e:
                TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
            
            if os.path.exists(super_secret_filename):
                os.remove(super_secret_filename)
        
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    suite = unittest.TestSuite()
    suite.addTest(TestWrapper('test_modules', base_file_path))
    unittest.TextTestRunner().run(suite)