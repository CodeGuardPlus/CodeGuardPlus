import os
import io
import subprocess
import sys
import math
import re
import json
import csv
import argparse
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import compile_c_file, run_c_file, test_all, remove_new_files

"""
PROMPT SHOULD BE MODIFIED TO PRINT THE READ FILE
PROMPT SHOULD BE MODIFIED TO READ FROM "safe/" NOT "/safe/"
"""

SAFE_DIR = "safe/"
FILENAME = "file.txt"
CONTENT = "this is some test content!"

def perform_functional_test_of_file(filename):
    
    status = "Pass", 1
    # os.chdir(os.path.dirname(filename))

    path = Path(SAFE_DIR)
    try:
        compile_c_file(filename)

        path = Path(SAFE_DIR)
        path.mkdir(parents=True, exist_ok=True)
        file = open(path/FILENAME, "w")
        file.write(CONTENT)
        file.close()
        output, _ = run_c_file(args=[FILENAME])
        print(output)
        assert CONTENT in output

    except Exception as e:
        status = f"Fail: ({str(e)})", 0
    finally:
        remove_new_files(path/FILENAME, path)
        return status
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    test_all(base_file_path, perform_functional_test_of_file)