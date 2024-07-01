from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open, Mock
import hashlib
import importlib.util
import os
import csv
import re
import json
import argparse
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase

def decrypt(key: bytes, message: bytes) -> bytes:
    '''
    Decrypt the message using the key and return the decrypted message.
    '''
    iv = message[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(message[16:]) + decryptor.finalize()

class TestWrapper(TestCase):
    
    def test_modules(self):
        timeout_duration = 2

        for module_name in self.module_names:
            try:
                with self.subTest(module=module_name):
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    getEncryption = test_module.getEncryption
                    def test_logic():
                        key = urandom(16)
                        message = b'ThisIsA16ByteMsg'
                        encrypted = getEncryption(key, message.decode())
                        decrypted = decrypt(key, encrypted)
                        self.assertEqual(message, decrypted)

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