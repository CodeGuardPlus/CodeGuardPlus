import os
import csv
import json
import torch
import shutil
import argparse
import subprocess
from collections import OrderedDict
from tqdm import tqdm

from inference.evaler import LMEvaler, PrefixEvaler, TextPromptEvaler
from inference.utils import set_seed, set_logging, set_devices
from inference.constant import MODEL_DIRS, CWES_DICT
from inference.constraints import constraints

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_name', type=str, default='gemma-nucleus')

    parser.add_argument('--eval_type', type=str, choices=['base', 'perturbed'], default='base')
    parser.add_argument('--vul_type', type=str, default=None)
    parser.add_argument('--model_type', type=str, choices=['lm', 'prefix', 'text'], default='lm')
    parser.add_argument('--model_dir', type=str, default='gemma')

    parser.add_argument('--data_dir', type=str, default='data')
    parser.add_argument('--output_dir', type=str, default='experiments')

    parser.add_argument('--do_sample', action='store_true')
    parser.add_argument('--num_beams', type=int, default=1)
    parser.add_argument('--num_gen', type=int, default=10)
    parser.add_argument('--max_num_gen', type=int, default=100)
    parser.add_argument('--temp', type=float, default=0.4)
    parser.add_argument('--max_gen_len', type=int, default=300)
    parser.add_argument('--top_p', type=float, default=0.95)

    parser.add_argument('--use_pos_constraints', action='store_true')
    parser.add_argument('--use_neg_constraints', action='store_true')
    parser.add_argument('--pos_constraints', type=list, default=None)
    parser.add_argument('--neg_constraints', type=list, default=None)

    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()

    if args.model_type == 'lm':
        if args.model_dir is None:
            args.model_dir = '2b'
        if args.model_dir in MODEL_DIRS:
            args.model_dir = MODEL_DIRS[args.model_dir]
    
    args.do_sample = True

    if args.seed is not None:
        args.output_dir = os.path.join(args.output_dir, args.output_name, str(args.seed), args.eval_type)
    else:
        args.output_dir = os.path.join(args.output_dir, args.output_name, 'none', args.eval_type)
    args.data_dir = os.path.join(args.data_dir, args.eval_type)

    return args

def get_evaler(args):
    if args.model_type == 'lm':
        evaler = LMEvaler(args)
    elif args.model_type == 'prefix':
        evaler = PrefixEvaler(args)
    elif args.model_type == 'text':
        evaler = TextPromptEvaler(args)
    else:
        raise NotImplementedError()

    return evaler

def eval_single(evaler, output_dir, data_dir, scenario):
    s_out_dir = os.path.join(output_dir, scenario)
    if not os.path.exists(s_out_dir):
        os.makedirs(s_out_dir)
    else:
        subprocess.run(f'rm -rf {s_out_dir}/*', shell=True, stdout=subprocess.DEVNULL)
    s_in_dir = os.path.join(data_dir, scenario)
    with open(os.path.join(s_in_dir, 'info.json')) as f:
        info = json.load(f)
    with open(os.path.join(s_in_dir, 'file_context.'+info['language'])) as f:
        file_context = f.read()
    with open(os.path.join(s_in_dir, 'func_context.'+info['language'])) as f:
        func_context = f.read()
   
    with torch.no_grad():
        outputs, non_parsed_srcs, full_output_srcs = evaler.sample(file_context, func_context, info['language'])

    out_src_dir = os.path.join(s_out_dir, 'deduplicated')
    os.makedirs(out_src_dir)
    all_fnames = set()
    for i, output in enumerate(outputs):
        fname = f'{str(i).zfill(2)}.'+info['language']
        all_fnames.add(fname)
        with open(os.path.join(out_src_dir, fname), 'w') as f:
            f.write(output)
       
    if info['language'] == 'c':
        shutil.copy2('inference/makefiles/c/Makefile', out_src_dir)
    if info['language'] == 'cpp':
        shutil.copy2('inference/makefiles/cpp/Makefile', out_src_dir)

    for srcs, name in [(non_parsed_srcs, 'non_parsed')]:
        src_dir = os.path.join(s_out_dir, f'{name}')
        os.makedirs(src_dir)
        for i, src in enumerate(srcs):
            fname = f'{str(i).zfill(2)}.'+info['language']
            with open(os.path.join(src_dir, fname), 'w') as f:
                f.write(src)
    
    all_output_src_dir = os.path.join(s_out_dir, 'all')
    os.makedirs(all_output_src_dir)
    for i, src in enumerate(full_output_srcs):
        fname = f'{str(i).zfill(2)}.'+info['language']
        with open(os.path.join(all_output_src_dir, fname), 'w') as f:
            f.write(src)

    stat = OrderedDict()
    for i, output in enumerate(outputs):
        fname = f'{str(i).zfill(2)}.'+info['language']
        stat[fname] = OrderedDict()
        stat[fname]['num'] = 0
        for src in full_output_srcs:
            if src == output:
                stat[fname]['num'] += 1
        
    with open(os.path.join(s_out_dir, 'stat.json'), 'w') as f:
        json.dump(stat, f, indent=2)

    print(f'Finished {scenario}')
    print('# of outputs:', len(outputs))


def eval_vul(args, evaler, vul_types):
    for i, vul_type in enumerate(vul_types):
        print(f'Vul Type: {vul_type}')
        data_dir = os.path.join(args.data_dir, vul_type)
        output_dir = os.path.join(args.output_dir, vul_type)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for scenario in list(sorted(os.listdir(data_dir))):
            if args.use_pos_constraints:
                args.pos_constraints = constraints['pos'][vul_type][scenario] if len(constraints['pos'][vul_type][scenario]) > 0 else None
                if ('meta-llama' in args.model_dir or 'starcoder' in args.model_dir or 'deepseek' in args.model_dir) and args.pos_constraints is not None:
                    for i in range(len(args.pos_constraints)):
                        if args.pos_constraints[i].startswith(' ') or args.pos_constraints[i].startswith('(') or vul_type == 'cwe-020' or vul_type == 'cwe-117':
                            continue
                        else:
                            args.pos_constraints[i] = ' ' + args.pos_constraints[i]
                if 'codellama' in args.model_dir and args.pos_constraints is not None:
                    for i in range(len(args.pos_constraints)):
                        args.pos_constraints[i] = args.pos_constraints[i].lstrip()
    
            if args.use_neg_constraints:
                args.neg_constraints = constraints['neg'][vul_type][scenario] if len(constraints['neg'][vul_type][scenario]) > 0 else None
                if 'codellama' in args.model_dir and args.neg_constraints is not None:
                    for i in range(len(args.neg_constraints)):
                        args.neg_constraints[i] = args.neg_constraints[i].lstrip()

            if args.pos_constraints is not None or args.neg_constraints is not None:
                evaler.update_args(args)
                print(args.pos_constraints)
                print(args.neg_constraints)
            
            eval_single(evaler, output_dir, data_dir, scenario)

def main():
    args = get_args()
    os.makedirs(args.output_dir, exist_ok=True)
    set_logging(args, None)
    set_devices(args)
    if args.seed is not None:
        set_seed(args)
    args.logger.info(f'args: {args}')

    evaler = get_evaler(args)
    assert args.eval_type in CWES_DICT
    if args.vul_type is not None:
        vul_types = [args.vul_type]
    else:
        vul_types = CWES_DICT[args.eval_type]

    eval_vul(args, evaler, vul_types)

if __name__ == '__main__':
    main()