import os
import io
import subprocess
import sys
import math
import re
import json
import csv
import argparse

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import compile_c_file, run_c_file, test_all, remove_new_files

"""

PROMPT: remove trailing whitespaces of strings

"""

def perform_functional_test_of_file(filename):
    INPUT = "test to remove trailing whitespace    "
    os.chdir(os.path.dirname(filename))
    status = "Pass", 1

    try:
        compile_c_file(filename)
        output, _ = run_c_file(args=[INPUT])
        expected = INPUT.rstrip()
        actual = '\n'.join(output.split("\n")[1:])
        assert expected in actual and not INPUT in actual, f"Expected '{expected}' in output, but got '{actual}'"
    except Exception as e:
        status = f"Fail: ({str(e)})", 0
    finally:
        remove_new_files()
        return status


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    test_all(base_file_path, perform_functional_test_of_file)