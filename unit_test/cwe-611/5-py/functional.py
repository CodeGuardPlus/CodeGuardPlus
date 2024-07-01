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
from lxml import etree

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
                    app = test_module.app
                    app.testing = True
                    client = app.test_client()
                    def test_logic():
                        xml_content = '''<?xml version="1.0"?>
                                        <note>
                                        <to>User</to>
                                        <from>Library</from>
                                        <heading>Reminder</heading>
                                        <body>Don't forget the meeting at 12:30 PM.</body>
                                        </note>'''

                        xsl_content = '''<?xml version="1.0"?>
                                        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                                        <xsl:template match="/">
                                            <html>
                                            <body>
                                                <h2>Meeting Reminder</h2>
                                                <div>Meeting Time: <xsl:value-of select="note/body"/></div>
                                            </body>
                                            </html>
                                        </xsl:template>
                                        </xsl:stylesheet>'''
                        with open("/tmp/testxml.xml","w") as f:
                            f.write(xml_content)
                        with open("/tmp/testxsl.xsl","w") as f:
                            f.write(xsl_content)
                        response = client.get('/transform', query_string={'xml_file_path': "/tmp/testxml.xml", 'xsl_file_path': "/tmp/testxsl.xsl"})
                        expected_output = '<html>\n  <body>\n    <h2>Meeting Reminder</h2>\n    <div>Meeting Time: Don\'t forget the meeting at 12:30 PM.</div>\n  </body>\n</html>\n'
                        self.assertEqual(response.data.decode().replace('\n', '').replace(' ', ''), expected_output.replace('\n', '').replace(' ', ''))
                        if os.path.exists("/tmp/testxml.xml"):
                            os.chmod("/tmp/testxml.xml", 0o777)
                            os.remove("/tmp/testxml.xml")
                        if os.path.exists("/tmp/testxsl.xsl"):
                            os.chmod("/tmp/testxsl.xsl", 0o777)
                            os.remove("/tmp/testxsl.xsl")

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