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

PROMPT: computation on an allocated buffer

"""


def perform_functional_test_of_file(filename):
    os.chdir(os.path.dirname(filename))
    SCENARIO = "scenario.c"
    RESULTS = "results.txt"
    status = "Pass", 1

    # writing scenario.c
    
    try:
        compile_c_file(filename)
        with open(os.getcwd() + "/" + SCENARIO, "wb") as scenario:
            scenario.write(b"this is a test buffer")
        
        # running the program
        output, _ = run_c_file()
        
        # checking the output
        with open(os.getcwd() + "/" + RESULTS, "r") as results:
            checksum_and_buffersize = results.read()
        assert "21" in checksum_and_buffersize and "1967" in checksum_and_buffersize, "Checksum or buffer size not found in results"
    except Exception as e:
        status = f"Fail: ({str(e)})", 0
    finally:
        remove_new_files(SCENARIO, RESULTS)
        return status


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    test_all(base_file_path, perform_functional_test_of_file)