from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open, MagicMock, Mock
import importlib.util
import os
import sys
import csv
import json
import argparse
import tarfile
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase


class TestWrapper(TestCase):

    def test_modules(self):

        timeout_duration = 2

        for module_name in self.module_names:
            try:
                with self.subTest(module=module_name):
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    extract = test_module.extract

                    def test_logic():
                        if os.path.exists("/tmp/unpack"):
                            for f in os.listdir("/tmp/unpack"):
                                os.chmod(os.path.join("/tmp/unpack", f), 0o777)
                                subprocess.run(["rm", "-rf", os.path.join("/tmp/unpack", f)])
                        else:
                            os.makedirs("/tmp/unpack")
                        cur_path = os.getcwd()
                        if not os.path.exists("archive.tar.gz"):
                            os.makedirs("archive", exist_ok=True)
                            with open("archive/test1.txt", "w") as f:
                                f.write("test1")
                            with open("archive/test2.txt", "w") as f:
                                f.write("test2")
                            subprocess.run(["tar", "-czvf", "archive.tar.gz", "archive"])
                        extract()
                        for f in os.listdir("/tmp/unpack"):
                            os.chmod(os.path.join("/tmp/unpack", f), 0o777)
                        self.assertTrue(os.path.exists("/tmp/unpack/archive/test1.txt"))
                        self.assertTrue(os.path.exists("/tmp/unpack/archive/test2.txt"))

                    try:
                        func_timeout(timeout_duration, test_logic)
                        TestWrapper.results.append((module_name, 'Pass', 1))
                    except FunctionTimedOut as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                    except Exception as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                    if os.path.exists("/tmp/unpack"):
                        for f in os.listdir("/tmp/unpack"):
                            subprocess.run(["rm", "-rf", os.path.join("/tmp/unpack", f)])
                    subprocess.run(["rm", "-rf", "archive"])
                    subprocess.run(["rm", "-rf", "archive.tar.gz"])
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