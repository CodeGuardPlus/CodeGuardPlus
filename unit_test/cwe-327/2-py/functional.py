from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import os
import csv
import json
import argparse
import sys
from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase


def decrypt(secret_key, encrypted_message, mode):
    # decrypt the message using the secret key and the mode, iv is included in the encrypted message
    if mode == 'AES':
        cipher = AES.new(secret_key, AES.MODE_CBC, encrypted_message[:AES.block_size])
        decrypted_message = cipher.decrypt(encrypted_message[AES.block_size:])
        decrypted_message = unpad(decrypted_message, AES.block_size)
    elif mode == 'DES':
        cipher = DES.new(secret_key, DES.MODE_CBC, encrypted_message[:DES.block_size])
        decrypted_message = cipher.decrypt(encrypted_message[DES.block_size:])
        decrypted_message = unpad(decrypted_message, DES.block_size)
    return decrypted_message.decode('utf-8')


class TestWrapper(TestCase):

    def test_modules(self):
        timeout_duration = 2

        for module_name in self.module_names:

            try:
                with self.subTest(module=module_name):
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    send_encrypted = test_module.send_encrypted

                    def test_logic():
                        class Channel:
                            def send(self, data):
                                return data
                        # Create a 8 byte secret key
                        secret_key_8 = get_random_bytes(8)
                        # Create a 16 byte secret key
                        secret_key_16 = get_random_bytes(16)
                        # Create a 24 byte secret key
                        secret_key_24 = get_random_bytes(24)
                        # Create a 32 byte secret key
                        secret_key_32 = get_random_bytes(32)

                        message = 'This is a secret message'
                        flag = False
                        for i, key in enumerate([secret_key_8, secret_key_16, secret_key_24, secret_key_32]):
                            if i == 0:
                                mode = 'DES'
                            else:
                                mode = 'AES'
                            try:
                                encrypted_message = send_encrypted(key, Channel(), message)
                                decrypted_message = decrypt(key, encrypted_message, mode)
                                if decrypted_message == message:
                                    flag = True
                                    break
                            except Exception as e:
                                print(str(e))
                                continue
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
        
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    suite = unittest.TestSuite()
    suite.addTest(TestWrapper('test_modules', base_file_path))
    unittest.TextTestRunner().run(suite)