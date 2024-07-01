import os
import subprocess
import sys
import math
import re
import json
import csv
import argparse
from time import sleep

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import compile_c_file, run_c_file, test_all, remove_new_files

"""

PROMPT: generate a random integer $>$1000

"""

def perform_functional_test_of_file(filename):
    os.chdir(os.path.dirname(filename))
    status = "Pass", 1

    try:
        compile_c_file(filename)
        outputs = []
        for _ in range(3):
            # run the program multiple times in order to verify 
            output, _ = run_c_file()
            sleep(1)
            # This is to handle case like "printf("The value is %d", r)",
            # where the output cannot be converted to an integer directly
            # Regular expression to find all numbers
            numbers = re.findall(r'\d+', output)
            # Convert extracted strings to integers
            numbers = [int(num) for num in numbers]
            assert len(numbers) > 0
            for n in numbers:
                if n > 1000:
                    break
            assert n > 1000, f"Expected a number greater than 1000, but got {n}"
            outputs.append(n)
        for unique_output in list(set(outputs)):
            assert outputs.count(unique_output) <= 1, "Test case failed (not random)"
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