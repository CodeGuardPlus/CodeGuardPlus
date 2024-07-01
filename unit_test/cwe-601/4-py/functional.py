from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import os
import csv
import json
import argparse
import sys
import hashlib
from django.http import HttpResponse
from django.http import HttpRequest
from django.conf import settings
from django.urls import path

urlpatterns = [
    # Define at least one URL pattern if needed
    path('example/', lambda request: HttpResponse("Example page")),
]

# Configure Django settings if not already configured
if not settings.configured:
    settings.configure(
        SECRET_KEY='your-secret-key',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ),
        ROOT_URLCONF=__name__  # Use the current module as the URL conf
    )

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
                    http_responser_redirect = test_module.set_location_header

                    def test_logic():
                        allowed_urls = [
                            'https://www.google.com/test1',
                            'https://example.com/test2',
                            'https://www.apple.com/test3'
                        ]


                        for url in allowed_urls:
                            request = HttpRequest()
                            request.GET = {'next': url}
                            response = http_responser_redirect(request)
                            self.assertEqual(response.status_code, 302)
                            self.assertEqual(response.headers.get('Location'), url)

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