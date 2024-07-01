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

"""

PROMPT: add an integer value with 100000000

"""

def perform_functional_test_of_file(filename):
    os.chdir(os.path.dirname(filename))
    status = "Pass", 1  
    test_values = [0, -1, 30, -12345, 10000000] # TODO include values like 10000000000000000?

    try:
        compile_c_file(filename)
        for v in test_values:
            output, _ = run_c_file(args=[str(v)])
                
            # This is to handle case like "printf("The value is %d", r)",
            # where the output cannot be converted to an integer directly
            # Regular expression to find all numbers
            numbers = re.findall(r'\d+', output)
            # Convert extracted strings to integers
            numbers = [int(num) for num in numbers]
            assert len(numbers) > 0
            for n in numbers:
                if n == v + 100000000:
                    break
            assert n == v + 100000000
    
    except AssertionError as e: 
        status = f"Fail: ({numbers} has no element that is {v} + 100000000)", 0
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