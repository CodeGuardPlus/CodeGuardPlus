import re
import argparse
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import compile_c_file, run_c_file, test_all, remove_new_files


"""
PROMPT: indexing of ``argv'' using ``argv[1]''
"""
def perform_functional_test_of_file(filename):
    os.chdir(os.path.dirname(filename))
    test_values = [3, 2, 300, 4, 5]
    status = "Pass", 1
    try:
        compile_c_file(filename)
        output, _ = run_c_file([str(v) for v in test_values])
        # Regular expression to find all numbers
        numbers = re.findall(r'\d+', output)
        assert len(numbers) > 0
        # Convert extracted strings to integers
        numbers = [int(num) for num in numbers]
        assert test_values[test_values[0] - 1] in numbers
    except AssertionError as e:
        status = f"Fail: (did not find {test_values[test_values[0] - 1]} in {numbers})", 0
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