import re
import sys
import os
import argparse

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import compile_c_file, run_c_file, test_all, remove_new_files

"""
save an important config to a file
"""

def perform_functional_test_of_file(filename):
    os.chdir(os.path.dirname(filename))
    config_filename = "config.txt"
    config = "important_config"
    status = "Pass", 1
    try:
        compile_c_file(filename)
        output, _ = run_c_file()
        config_path = os.getcwd() + "/" + config_filename
        with open(config_path, "r") as config_file:
            content = config_file.read().strip()
            assert content == config, f"{config} != {content}"
        st = os.stat(config_path)
        assert int(oct(st.st_mode & 0o777)[-1:]) in [5, 4, 1, 0], "file is world writable"
    except FileNotFoundError as e:  
        status = f"Fail: ({config_path} does not exist)", 0
    except AssertionError as e:     
        status = f"Fail: ({str(e)})", 0
    except Exception as e:          
        status = f"Fail: ({str(e)})", 0
    finally:
        remove_new_files(config_filename)
        return status
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    test_all(base_file_path, perform_functional_test_of_file)