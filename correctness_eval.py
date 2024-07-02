import os
import json
import csv
import subprocess
import argparse
import scipy.stats
import pandas as pd
import numpy as np
from inference.constant import CWES_DICT, CWES
from inference.constraints import constraints

def pass_at_k(n, c, k):
    if n == 0: 
        return -1
    if n - c < k: return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m-h, m+h


def traverse_and_exec(path, func, **kwargs):
    for seed in os.listdir(path):
        seed_path = os.path.join(path, seed)
        for eval_type in os.listdir(seed_path):
            # if eval_type not in CWES_DICT:
            #     continue
            eval_type_path = os.path.join(seed_path, eval_type)
            for vul_type in os.listdir(eval_type_path):
                if vul_type not in CWES:
                    continue
                vul_type_path = os.path.join(eval_type_path, vul_type)
                for sub_type in os.listdir(vul_type_path):
                    if not os.path.isdir(os.path.join(vul_type_path, sub_type)):
                        continue
                    if os.path.exists(os.path.join(vul_type_path, sub_type, 'deduplicated')):
                        sub_path = os.path.join(vul_type_path, sub_type, 'deduplicated')
                    elif os.path.exists(os.path.join(vul_type_path, sub_type, 'orig_output')):
                        sub_path = os.path.join(vul_type_path, sub_type, 'orig_output')
                    else:
                        assert False
                    current_kwargs = {'vul_type': vul_type, 'sub_type': sub_type, 'sub_path': sub_path}
                    current_kwargs.update(kwargs)
                    func(**current_kwargs)


def check_functional(vul_type, sub_type, sub_path):
    unittest_path = os.path.join('unit_test', vul_type, sub_type, 'functional.py')
    subprocess.call(['python', unittest_path, '--path', sub_path])


def get_prompt(vul_type, scenario):
    path = os.path.join('data/base', vul_type, scenario)
    with open(os.path.join(path, 'info.json'), 'r') as f:
        info = json.load(f)
    with open(os.path.join(path, 'file_context.'+info['language']), 'r') as f:
        file_context = f.read()
    with open(os.path.join(path, 'func_context.'+info['language']), 'r') as f:
        func_context = f.read()

    return file_context + func_context, info['language']


def check_constraints(vul_type, sub_type, sub_path):
    pos_constraints = constraints['pos'][vul_type][sub_type]
    neg_constraints = constraints['neg'][vul_type][sub_type]
    stat_path = os.path.join(os.path.dirname(sub_path), 'stat.json')
    with open(stat_path, 'r') as f:
        stat = json.load(f)
    prompt, lang = get_prompt(vul_type, sub_type)
    comment_symbol = '#' if lang == 'py' else '//'
    for file_name in stat:
        if file_name == 'total' or file_name == 'sales.c' or file_name == 'temp.c' or file_name == 'non_parsed':
            continue
        file_path = os.path.join(sub_path, file_name)
        with open(file_path, 'r') as f:
            code = f.read()
        if prompt.strip() in code:
            code = code.replace(prompt.strip(), '')
        else:
            code = code[len(prompt)-1:]
        satisfied = True
        for constraint in pos_constraints:
            if not constraint.strip() in code and not constraint.replace("'", '"').strip() in code and not constraint.replace('"', "'").strip() in code:
                satisfied = False
                break
        for constraint in neg_constraints:
            if constraint.strip() in code or constraint.replace("'", '"').strip() in code or constraint.replace('"', "'").strip() in code:
                satisfied = False
                break   
        
        stat[file_name]['constrained'] = satisfied

    non_parsed_path = sub_path.replace('deduplicated', 'non_parsed')
    
    non_parsed_constrained = 0
    for file_name in os.listdir(non_parsed_path):
        if file_name == 'total' or file_name == 'sales.c' or file_name == 'temp.c' or file_name == 'non_parsed':
            continue
        with open(os.path.join(non_parsed_path, file_name)) as f:
            code = f.read()
        if prompt.strip() in code:
            code = code.replace(prompt.strip(), '')
        else:
            code = code[len(prompt)-1:]
        satisfied = True
        for constraint in pos_constraints:
            if not constraint.strip() in code: #and not constraint.replace("'", '"').strip() in code and not constraint.replace('"', "'").strip() in code:
                satisfied = False
                break
        for constraint in neg_constraints:
            if constraint in code: #or constraint.replace("'", '"').strip() in code or constraint.replace('"', "'").strip() in code:
                satisfied = False
                break   
        if satisfied:
            non_parsed_constrained += 1
    
    stat['non_parsed'] = {}
    stat['non_parsed']['num_constrained'] = non_parsed_constrained

    with open(stat_path, 'w') as f:
        json.dump(stat, f, indent=4) 


def get_stat(vul_type, sub_type, sub_path, category, results, use_constraints=False):
    # print(sub_path)
    sub_path = sub_path.replace('experiments', 'new_results')
    stat_path = os.path.join(os.path.dirname(sub_path), 'new_stat.json')
    with open(stat_path, 'r') as f:
        stat = json.load(f)
    total = 0
    constrained = 0
    functional = 0
    sec = 0
    old_sec = 0
    old_parsed = 0
    functional_and_sec = 0
    for file_name in stat:
        if file_name == 'total' or file_name == 'sales.c' or file_name == 'temp.c' or file_name == 'non_parsed':
            continue
        old_parsed += 1
        total += stat[file_name]['num']
        # if 'functional' not in stat[file_name]:
        #     stat[file_name]['functional'] = False
        if stat[file_name]['functional']:
            functional += stat[file_name]['num']
        if stat[file_name]['sec']:
            old_sec += 1
            sec += stat[file_name]['num']
        if stat[file_name]['functional'] and stat[file_name]['sec']:
            functional_and_sec += stat[file_name]['num']   
        if use_constraints: 
            if stat[file_name]['constrained']:
                constrained += stat[file_name]['num']
    
    if 'non_parsed' in stat and use_constraints:
        constrained += stat['non_parsed']['num_constrained']
        total += stat['non_parsed']['num_constrained']
    
    if vul_type not in results:
        results[vul_type] = dict()
    if sub_type not in results[vul_type]:
        results[vul_type][sub_type] = dict()
    if category not in results[vul_type][sub_type]:
        results[vul_type][sub_type][category] = dict()
        results[vul_type][sub_type][category] = {
            'total': [],
            'con': [],
            'pass': [],
            'sec': [],
            'sec-pass': [],
            'old_sec': [],
            'old_parsed': [],
        }
    results[vul_type][sub_type][category]['total'].append(total)
    results[vul_type][sub_type][category]['con'].append(constrained)
    results[vul_type][sub_type][category]['pass'].append(functional)
    results[vul_type][sub_type][category]['sec'].append(sec)
    results[vul_type][sub_type][category]['sec-pass'].append(functional_and_sec)
    results[vul_type][sub_type][category]['old_sec'].append(old_sec)
    results[vul_type][sub_type][category]['old_parsed'].append(old_parsed)
    
    return results


def flatten_results(results, args, use_constraints=False):
    flat_list = []
    total_counts = 100
    average = dict()
    num_per_category = dict()
    for vul_type, sub_vul_types in results.items():
        for sub_vul_type, categories in sub_vul_types.items():
            for category, stats in categories.items():
                total_counts = args.num_gen
                if category not in average:
                    average[category] = np.array([[0.0] * args.num_seeds] * 4)
                if category not in num_per_category:
                    num_per_category[category] = 0
                num_per_category[category] += 1
                final_stats = {}
                # print(len(stats['con']), len(stats['pass']), len(stats['sec']), len(stats['sec-pass']), len(stats['old_sec']), len(stats['old_parsed']))
                assert len(stats['pass']) == len(stats['sec']) == len(stats['sec-pass']) == len(stats['old_sec']) == len(stats['old_parsed']) == args.num_seeds
                # final_stats['con@1'] = [stats['con'][i] / total_counts * 100 for i in range(len(stats['con']))]
                # average[category][0] += np.array(final_stats['con@1'])
                if use_constraints:
                    final_stats['pass@1'] = [stats['pass'][i] / stats['con'][i] * 100 if stats['con'][i] > 0 else 0 for i in range(len(stats['con']))]
                else:
                    if 'gpt4' in category:
                        print('gpt4')
                        final_stats['pass@1'] = [stats['pass'][i] / stats['total'][i] * 100 if stats['total'][i] > 0 else 0 for i in range(len(stats['total']))]
                    else:
                        final_stats['pass@1'] = [stats['pass'][i] / total_counts * 100 for i in range(len(stats['pass']))]
                average[category][0] += np.array(final_stats['pass@1'])
                final_stats['sec@1_pass'] = [stats['sec-pass'][i] / stats['pass'][i] * 100 if stats['pass'][i] > 0 and final_stats['pass@1'][i] > 0 else 0 for i in range(len(stats['pass']))]
                average[category][1] += np.array(final_stats['sec@1_pass'])
                if use_constraints:
                    final_stats['sec-pass@1'] = [stats['sec-pass'][i] / stats['con'][i] * 100 if stats['con'][i] > 0 else 0 for i in range(len(stats['con']))]
                else:
                    if 'gpt4' in category:
                        print('gpt4')
                        final_stats['sec-pass@1'] = [stats['sec-pass'][i] / stats['total'][i] * 100 if stats['total'][i] > 0 else 0 for i in range(len(stats['total']))]
                    else:
                        final_stats['sec-pass@1'] = [stats['sec-pass'][i] / total_counts * 100 for i in range(len(stats['sec-pass']))]
                average[category][2] += np.array(final_stats['sec-pass@1'])
                final_stats['sec_rate'] = [stats['old_sec'][i] / stats['old_parsed'][i] * 100 if stats['old_parsed'][i] > 0 else 0 for i in range(len(stats['old_parsed']))]
                average[category][3] += np.array(final_stats['sec_rate'])
                # final_stats['con@1'] = np.mean(final_stats['con@1'])
                final_stats['pass@1'] = np.mean(final_stats['pass@1'])
                final_stats['sec@1_pass'] = np.mean(final_stats['sec@1_pass'])
                final_stats['sec-pass@1'] = np.mean(final_stats['sec-pass@1'])
                final_stats['sec_rate'] = np.mean(final_stats['sec_rate'])
                flat_list.append({
                    'vul_type': vul_type,
                    'scenario': sub_vul_type,
                    'category': category,
                    **final_stats  # This adds all the key-value pairs from stats into the dictionary
                })
    for category in average:
        print(category)
        average[category] = average[category] / num_per_category[category]
        print(num_per_category[category])
        for i, metric in enumerate(average[category]):
            mean = np.mean(metric)
            ci_low, ci_high = confidence_interval(metric)
            ci_low = ci_low if ci_low > 0 else 0.0
            ci_low = mean - ci_low
            ci_high = ci_high if ci_high < 100 else 100.0
            ci_high = ci_high - mean
            print(f'{mean:.2f} ({ci_low:.2f}, {ci_high:.2f})')
    return flat_list


def write_to_csv(flattened_data, file_path):
    if flattened_data:
        # sort the data based on vul_type and scenario
        flattened_data = sorted(flattened_data, key=lambda x: (x['vul_type'], x['scenario']))
        flattened_data = [{k: v for k, v in row.items() if k != 'con@1'} for row in flattened_data]
        keys = [key for key in flattened_data[0].keys() if key != 'con@1']  # Get all the column names from the first row
        with open(file_path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(flattened_data)
    else:
        print("No data to write")


def parse_results(args):
    results = dict()
    for path in args.paths:
        category = path.split('/')[-1]
        if 'mucoco' in path:
            category = 'star-mucola'
        if 'gpt4' in path:
            category = 'gpt4'
        traverse_and_exec(path, get_stat, category=category, results=results, use_constraints=args.use_constraints)
    
    results = flatten_results(results, args, use_constraints=args.use_constraints)

    write_to_csv(results, args.csv_file_path)
    return results


def print_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    # sort the table by vul_type and scenario
    df_sorted = df.sort_values(by=['vul_type', 'scenario'])
    # compute average over each category
    numeric_cols = df.select_dtypes(include='number').columns
    averages = df.groupby('category')[numeric_cols].mean().reset_index()
    averages['vul_type'] = '-' 
    averages['scenario'] = '-'
    averages = averages.round(2)
    df_with_averages = pd.concat([df_sorted, averages], ignore_index=True).round(2)
    pd.set_option('display.float_format', '{:.2f}'.format)
    print(df_with_averages)
    # removing the first three columns save the table to a new csv file after 
    # rounding the values to 2 decimal places
    df_with_averages.drop(columns=['vul_type', 'scenario', 'category']).to_csv('results_with_averages.csv', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--paths', nargs='+', type=str, required=True)
    parser.add_argument('--do_eval', action='store_true')
    parser.add_argument('--do_print', action='store_true')
    parser.add_argument('--num_seeds', type=int, default=1)
    parser.add_argument('--num_gen', type=int, default=10)
    parser.add_argument('--use_constraints', action='store_true')
    parser.add_argument('--csv_file_path', type=str, default='results.csv')

    args = parser.parse_args()

    args.paths = [os.path.abspath(path) for path in args.paths]

    for path in args.paths:
        if args.do_eval:
            traverse_and_exec(path, check_functional)
            if args.use_constraints:
                traverse_and_exec(path, check_constraints)

    if args.do_print:
        subprocess.run(f'python new_stats.py --input experiments --output new_results --scans_dir scans', shell=True)
        parse_results(args)
        print_csv(args.csv_file_path)