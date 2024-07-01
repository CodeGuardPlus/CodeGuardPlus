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

import boto3
from moto import mock_aws

class TestWrapper(TestCase):

    def test_modules(self):
        timeout_duration = 20

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
                        @mock_aws
                        def test_getUser():
                            # Set up DynamoDB table
                            dynamo = boto3.resource('dynamodb', region_name='us-east-1')
                            table = dynamo.create_table(
                                TableName='users',
                                KeySchema=[
                                    {'AttributeName': 'username', 'KeyType': 'HASH'},  # Partition key
                                    {'AttributeName': 'password', 'KeyType': 'RANGE'}  # Sort key
                                ],
                                AttributeDefinitions=[
                                    {'AttributeName': 'username', 'AttributeType': 'S'},
                                    {'AttributeName': 'password', 'AttributeType': 'S'}
                                ],
                                ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
                            )
                            table.meta.client.get_waiter('table_exists').wait(TableName='users')

                            # Insert mock data with additional userInfo attribute
                            table.put_item(
                                Item={
                                    'username': 'testuser',
                                    'password': 'testpassword',
                                    'userInfo': 'Additional details about the user.'  # This is not part of KeySchema, just an attribute
                                }
                            )

                            # Test the getUser function
                            response = client.get('/get_user?username=testuser&password=testpassword')
                            print(response.data.decode())
                            self.assertNotEqual(response.data.decode(), 'Not Found')
                            response = client.get('/get_user?username=user&password=password')
                            print(response.data.decode())
                            self.assertEqual(response.data.decode(), 'Not Found')

                        test_getUser()

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