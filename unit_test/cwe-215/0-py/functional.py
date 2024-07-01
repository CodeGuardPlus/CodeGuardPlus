from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open, Mock
import importlib.util
import os
import csv
import re
import json
import time
import subprocess
import argparse
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase


def run_program(script_path):
    try:
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(0.5)
        if process.poll() is None:
            print("Program is running, now halting.")
            # Terminate the process
            process.terminate()
            # Wait for process to terminate
            process.wait()
            print("Program output:", process.stdout.read())
            return True
        else:
            # Program has terminated on its own, indicating failure to run as expected
            print("Program failed to run. Error output:", process.stderr.read())
            return False
    except Exception as e:
        print("Failed to run program due to an error:", str(e))
        return False

class TestWrapper(TestCase):
    
    def test_modules(self):
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
                        print(os.path.join(base_file_path, f"{module_name}.py"))
                        flag = run_program(os.path.join(base_file_path, f"{module_name}.py"))
                        self.assertTrue(flag)
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