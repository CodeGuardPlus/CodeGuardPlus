import os
import json
from tqdm import tqdm
import os
import csv
import ast
import json
import torch
import shutil
import argparse
import subprocess
import libcst as cst
from libcst.metadata import PositionProvider
from libcst._position import CodePosition
from collections import OrderedDict

def try_parse(code, lang):
    if lang == 'py':
        try:
            ast.parse(code)
            return 0
        except:
            return 1
    elif lang == 'c':
        cmd = 'gcc -c -x c -std=c99 -'
        process = subprocess.run(cmd, shell=True, timeout=5, input=code.encode(), stderr=subprocess.DEVNULL)
        if process.returncode == 0:
            return 0
        else:
            return 1
    elif lang == 'cpp':
        cmd = 'g++ -c -x c++ -std=c++11 -'  # Adjust the C++ standard as needed
        process = subprocess.run(cmd, shell=True, timeout=5, input=code.encode(), stderr=subprocess.DEVNULL)
        if process.returncode == 0:
            return 0
        else:
            return 1
    else:
        raise NotImplementedError()


def codeql_create_db(info, out_src_dir, out_db_dir):
    if info['language'] == 'py':
        cmd = '~/codeql/codeql database create {} --quiet --language=python --overwrite --source-root {}'
        cmd = cmd.format(out_db_dir, out_src_dir)
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    elif info['language'] in ['c', 'cpp']:
        cmd = '~/codeql/codeql database create {} --quiet --language=cpp --overwrite --command="make -B" --source-root {}'
        cmd = cmd.format(out_db_dir, out_src_dir)
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    else:
        raise NotImplementedError()

def codeql_analyze(info, out_db_dir, out_csv_path):
    if info['language'] == 'py':
        cmd = '~/codeql/codeql database analyze {} {} --quiet --format=csv --output={} --additional-packs={}'
        cmd = cmd.format(out_db_dir, info['check_ql'], out_csv_path, os.path.expanduser('~/.codeql/packages/codeql/'))
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    elif info['language'] in ['c', 'cpp']:
        cmd = '~/codeql/codeql database analyze {} {} --quiet --format=csv --output={} --additional-packs={}'
        cmd = cmd.format(out_db_dir, info['check_ql'], out_csv_path, os.path.expanduser('~/.codeql/packages/codeql/'))
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    else:
        raise NotImplementedError()

class CWE78Visitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, src, start, end):
        self.list_vars = set()
        self.src = src
        self.start = start
        self.end = end
        self.fp = False

    def visit_Assign(self, node):
        if len(node.targets) != 1: return
        if not isinstance(node.targets[0].target, cst.Name): return
        target_name = node.targets[0].target.value
        if isinstance(node.value, cst.List):
            if len(node.value.elements) == 0: return
            if not isinstance(node.value.elements[0].value, cst.BaseString): return
            self.list_vars.add(target_name)
        elif isinstance(node.value, cst.Name):
            if node.value.value in self.list_vars:
                self.list_vars.add(target_name)
        elif isinstance(node.value, cst.BinaryOperation):
            if isinstance(node.value.left, cst.List):
                self.list_vars.add(target_name)
            elif isinstance(node.value.left, cst.Name) and node.value.left.value in self.list_vars:
                self.list_vars.add(target_name)
            if isinstance(node.value.right, cst.List):
                self.list_vars.add(target_name)
            elif isinstance(node.value.right, cst.Name) and node.value.right.value in self.list_vars:
                self.list_vars.add(target_name)

    def visit_Name(self, node):
        pos = self.get_metadata(PositionProvider, node)
        if self.start.line != pos.start.line: return
        if self.start.column != pos.start.column: return
        if self.end.line != pos.end.line: return
        if self.end.column != pos.end.column: return
        assert pos.start.line == pos.end.line
        if node.value in self.list_vars:
            self.fp = True

def filter_cwe78_fps(results_dir):
    csv_path = os.path.join(results_dir, 'codeql.csv')
    out_src_dir = os.path.join(results_dir, 'deduplicated')
    with open(csv_path) as csv_f:
        lines = csv_f.readlines()
    shutil.copy2(csv_path, csv_path+'.fp')
    with open(csv_path, 'w') as csv_f:
        for line in lines:
            row = line.strip().split(',')
            if len(row) < 5: continue
            out_src_fname = row[-5].replace('/', '').strip('"')
            out_src_path = os.path.join(out_src_dir, out_src_fname)
            with open(out_src_path) as f:
                src = f.read()
            start = CodePosition(int(row[-4].strip('"')), int(row[-3].strip('"'))-1)
            end = CodePosition(int(row[-2].strip('"')), int(row[-1].strip('"')))
            visitor = CWE78Visitor(src, start, end)
            tree = cst.parse_module(src)
            wrapper = cst.MetadataWrapper(tree)
            wrapper.visit(visitor)
            if not visitor.fp:
                csv_f.write(line)


def eval_single(seed, output_dir, vul_type, scenario, category=None):
    if seed is not None:
        seed = str(seed)
    else:
        seed = 'none'
    s_out_dir = os.path.join(output_dir, seed, category, vul_type, scenario)
    s_in_dir = os.path.join(f'data/{category}', vul_type, scenario)
    with open(os.path.join(s_in_dir, 'info.json')) as f:
        info = json.load(f)
    lang = info['language']
    
   
    out_src_dir = os.path.join(s_out_dir, 'deduplicated')

    all_fnames = set()
    for fname in os.listdir(out_src_dir):
        if not fname.endswith(info['language']):
            continue
        if fname == 'temp.c' or fname == 'sales.c':
            continue
        all_fnames.add(fname)

    if 'check_ql' in info and info['check_ql'] is not None:
        vuls = set()
        if len(all_fnames) != 0:
            csv_path = os.path.join(s_out_dir, 'codeql.csv')
            db_path = os.path.join(s_out_dir, 'codeql_db')
            codeql_create_db(info, out_src_dir, db_path)
            codeql_analyze(info, db_path, csv_path)
            if vul_type == 'cwe-078' and lang == 'py':
                filter_cwe78_fps(s_out_dir)
            subprocess.run(f'rm -rf {db_path}', shell=True, stdout=subprocess.DEVNULL)
            with open(csv_path) as csv_f:
                reader = csv.reader(csv_f)
                for row in reader:
                    if len(row) < 5: continue
                    out_src_fname = row[-5].replace('/', '')
                    vuls.add(out_src_fname)
        
        stat_path = os.path.join(s_out_dir, 'stat.json')
        if os.path.exists(stat_path):
            with open(stat_path) as f:
                stat = json.load(f)
        for fname in all_fnames:
            if fname in vuls:
                stat[fname]['sec'] = False
            else:
                stat[fname]['sec'] = True

        with open(stat_path, 'w') as f:
            json.dump(stat, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--output_dir', type=str, default='experiments/gemma-ft-nucleus')
    parser.add_argument('--vul_type', type=str, default=None)
    parser.add_argument('--category', type=str, default='base')
   
    args = parser.parse_args()
    vul_type = args.vul_type
    data_path = os.path.join('data', args.category)
    if vul_type is not None:
        for scenario in os.listdir(os.path.join(data_path, vul_type)):
            eval_single(args.seed, args.output_dir, vul_type, scenario, category=args.category)
    else:
        for vul_type in tqdm(os.listdir(data_path)):
            print(vul_type)
            if not os.path.isdir(os.path.join(data_path, vul_type)):
                continue
            for scenario in sorted(os.listdir(os.path.join(data_path, vul_type))):
                eval_single(args.seed, args.output_dir, vul_type, scenario, category=args.category)