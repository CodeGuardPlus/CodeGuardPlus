from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import os
import subprocess
import argparse
import json

### PYTHON TEST UTILS ###

class TestCase(unittest.TestCase):

    results = []
    base_file_path = None

    def __init__(self, method_name, base_file_path):
        super(TestCase, self).__init__(method_name)
        if TestCase.base_file_path is None:
            TestCase.base_file_path = base_file_path
        self.base_file_path = base_file_path
        self.module_names = []
        for file in os.listdir(base_file_path):
            if file.endswith(".py") and file != "__init__.py":
                if file[:-3] == 'functional':
                    continue
                self.module_names += [file[:-3]]
        self.module_names.sort()

    @classmethod
    def tearDownClass(cls):
        stat_path = os.path.join(os.path.dirname(cls.base_file_path), 'stat.json')
        # print(f"stat_path: {stat_path}")
        stat = None
        if os.path.exists(stat_path):
            with open(stat_path, 'r') as f:
                stat = json.load(f)
        
        num_total = 0
        num_passes = 0
        for module_name, status, score, *exception in cls.results:
            num_total += 1
            if exception:
                print(f"{module_name}: {status} - {exception[0]}")
                if stat is not None:
                    if module_name + '.py' in stat:
                        stat[module_name + '.py']['functional'] = False
                    else:
                        stat[module_name + '.c']['functional'] = False
            else:
                num_passes += 1
                if stat is not None:
                    if module_name + '.py' in stat:
                        stat[module_name + '.py']['functional'] = True
                    else:
                        stat[module_name + '.c']['functional'] = True

        # Print the summary after all tests
        print('\nTest Summary:')
        print(f'Total tests: {num_total}')
        print(f'Functional: {num_passes}')
        if stat is not None:
            with open(stat_path, 'w') as f:
                json.dump(stat, f, indent=4)

### C/C++ TEST UTILS ###

def compile_c_file(filename, cc="gcc", cc_args=["-std=c99", "-o", "a.out"], additonal_args=[]):
    # go to directory of filename
    if filename.endswith(".cpp"):
        cc = "g++"
        cc_args = ["-std=c++11", "-o", "a.out"]
    
    #compile the scenario
    subprocess.call([cc] + cc_args + [filename] + additonal_args, 
                    stderr=subprocess.PIPE, 
                    stdout=subprocess.PIPE)
    #check if the file was made
    if not os.path.isfile("a.out"):
        raise Exception("bad compile")
    
def remove_new_files(*args):
    for fname in list(args) + ["a.out"]:
        # reset the permission for the file
        if os.path.exists(fname):
            os.chmod(fname, 0o777)
        subprocess.call(["rm", fname], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)

def run_c_file(args=[], stdin=b""):
    proc = subprocess.run(["./a.out"] + args, # run file
                          input=stdin,
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          timeout=5)
    if proc.returncode != 0:
        raise Exception("program exited non zero")
    try:
        return proc.stdout.decode(), proc.stderr.decode()
    except:
        return proc.stdout, proc.stderr

def test_all(path, test):
    #get all the files in the directory
    files = os.listdir(path)
    files.sort()
    files = [f for f in files if f.endswith(".c") or f.endswith(".cpp") and f != "sales.c"]

    stat_path = os.path.join(os.path.dirname(path), 'stat.json')
    stat = None
    if os.path.exists(stat_path):
        with open(stat_path, 'r') as f:
            stat = json.load(f)
    
    num_passes = 0
    for f in files:
        filename = os.path.join(path, f)
        print("Testing %s..." % f)
        msg, result = test(filename)
        if result == 0:
            print(msg, result)
            if stat is not None:
                if f in stat:
                    stat[f]['functional'] = False
                else:
                    stat[f] = {'functional': False}
        else:
            assert msg == 'Pass'
            num_passes += 1
            if stat is not None:
                if f in stat:
                    stat[f]['functional'] = True
                else:
                    stat[f] = {'functional': True}


    # Print the summary after all tests
    print('\nTest Summary:')
    print(f'Total tests: {len(files)}')
    print(f'Functional: {num_passes}')

    if stat is not None:
        with open(stat_path, 'w') as f:
            json.dump(stat, f, indent=4)