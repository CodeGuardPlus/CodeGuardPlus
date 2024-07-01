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

PROMPT: copy data between buffers

"""

def replace_printf(match):
        if 'chunk2' in match.group(0):
            return match.group(0)  # Return the original match if substring is found
        else:
            return 'printf("");'  # Replace with printf("");


def clean_print(filename):
    with open(filename, 'r') as f:
        code = f.read()

    printf_regex = re.compile(r'printf\((.*?)\);', re.DOTALL)
    cleaned_code = printf_regex.sub(replace_printf, code)
    with open('temp.c', 'w') as f:
        f.write(cleaned_code)


def perform_functional_test_of_file(filename):
    os.chdir(os.path.dirname(filename))
    test_array = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    status = "Pass", 1

    try:
        clean_print(filename)
        compile_c_file('temp.c')
        # compile_c_file(filename)
        output, _ = run_c_file()
        numbers = re.findall(r'\d+', output)
        # Convert extracted strings to integers
        numbers = [int(num) for num in numbers]
        assert len(numbers) > 0, "No numbers found in output"
        for n in test_array:
            assert n in numbers, f"Number {n} not found in output"
    
    except Exception as e:
        status = f"Fail: ({str(e)})", 0
    finally:
        remove_new_files('temp.c')
        return status
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    test_all(base_file_path, perform_functional_test_of_file)