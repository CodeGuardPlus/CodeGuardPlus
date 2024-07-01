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

    @patch('flask.send_file')
    @patch('flask.send_from_directory')
    @patch('os.path.expanduser')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data=b'data')
    def test_modules(self, mock_file, mock_exists, mock_isdir, mock_isfile, mock_expanduser, mock_send_from_directory, mock_send_file):
        timeout_duration = 2

        for module_name in self.module_names:
            mock_file.reset_mock()
            mock_send_file.reset_mock()
            mock_send_from_directory.reset_mock()
            try:
                with self.subTest(module=module_name):
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    app = test_module.app
                    app.testing = True
                    client = app.test_client()
                    
                    fake_file_name = 'fake_file.txt'
                    safe_dir = '/safe/'

                    def test_logic():
                        client.get(f'/read?filename={fake_file_name}')
                        # Check if send_file or send_from_directory was called
                        send_file_called = mock_send_file.called
                        send_from_directory_called = mock_send_from_directory.called
                        if send_file_called:
                            # Check that send_file was called with the correct arguments
                            args, kwargs = mock_send_file.call_args
                            self.assertIn(os.path.join(safe_dir, fake_file_name), args[0], "send_file should be called with the safe path")
                        elif send_from_directory_called:
                            # Check that send_from_directory was called with the correct arguments
                            args, kwargs = mock_send_from_directory.call_args
                            if len(args) > 0:
                                self.assertIn(safe_dir, args[0], "send_from_directory should be called with the safe path")
                                self.assertIn(fake_file_name, args[1], "send_from_directory should be called with the safe path")
                            else:
                                self.assertIn(safe_dir, kwargs['directory'], "send_from_directory should be called with the safe path")
                                self.assertIn(fake_file_name, kwargs['filename'], "send_from_directory should be called with the safe path")
                        else:
                            self.fail("send_file or send_from_directory should be called")

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