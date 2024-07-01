import os
import sys
import ast
import torch
import random
import logging
import subprocess
import numpy as np

logger = logging.getLogger()

def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)

def set_logging(args, log_file):
    handlers = []
    handlers.append(logging.StreamHandler(stream=sys.stdout))
    if log_file is not None:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        level=logging.INFO,
        handlers=handlers
    )
    args.logger = logger

def set_devices(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    args.n_gpu = torch.cuda.device_count()
    args.device = device
    args.logger.info('Device: %s, n_gpu: %s', device, args.n_gpu)

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
        cmd = 'g++ -c -x c++ -std=c++11 -'
        process = subprocess.run(cmd, shell=True, timeout=5, input=code.encode(), stderr=subprocess.DEVNULL)
        if process.returncode == 0:
            return 0
        else:
            return 1
    else:
        raise NotImplementedError()

def check_constraints(code, pos_constraints, neg_constraints):
    satisfied = True
    if pos_constraints is not None:
        for constraint in pos_constraints:
            if not constraint.strip() in code:
                satisfied = False
                break
    if neg_constraints is not None:
        for constraint in neg_constraints:
            if constraint in code:
                satisfied = False
                break

    return satisfied