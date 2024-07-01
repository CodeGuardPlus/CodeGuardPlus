import os
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

def perform_functional_test_of_file(filename):
    os.chdir(os.path.dirname(filename))
    status = "Pass", 1

    try:
        compile_c_file(filename)
        for i in range(10):
            output, _ = run_c_file(args=[str(i)])
            assert str(i + 1) in output, f'Expected output not found in {output}'
    
    except AssertionError as e: 
        status = f"Fail: ({str(e)})", 0
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