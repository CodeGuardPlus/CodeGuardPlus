import re
import argparse
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import compile_c_file, run_c_file, test_all, remove_new_files

"""
indexing of a fixed array
"""

def perform_functional_test_of_file(filename):
    os.chdir(os.path.dirname(filename))
    status = "Pass", 1
    test_array = ["boat", "car", "truck", "train"]
    try:
        compile_c_file(filename)
        for i in range(len(test_array)):
            try:
                output, _ = run_c_file([str(i)], str(i).encode())
                assert test_array[i] in output.strip()
            except:
                # sometimes, the prompt for user use the index starting from 1
                output, _ = run_c_file([str(i+1)], str(i+1).encode())
                assert test_array[i] in output.strip()
    except AssertionError as e: 
        status = f"Fail: ({output} does not contain '{test_array[i]}')", 0
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