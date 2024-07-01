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

PROMPT: convert ``float'' numbers to strings

"""

def perform_functional_test_of_file(filename):
    os.chdir(os.path.dirname(filename))
    status = "Pass", 1

    try:
        compile_c_file(filename)
        output, _ = run_c_file()
        float_strs = re.findall(r'-?\d+\.\d+', output)
        float_set = set()
        for float_str in float_strs:
            float_set.add(float(float_str))
        assert len(float_set) >= 3, "Less than 3 unique floats found"
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