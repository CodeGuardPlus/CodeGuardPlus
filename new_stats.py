import os
import glob
import json
import argparse
from pathlib import Path
from tqdm import tqdm

def get_sonar_scans(base_path="scans"):
    scans = []
    for fname in os.listdir(base_path):
        if ".swp" in fname:
            continue
        with open(f"{base_path}/{fname}", "r") as file:
            print(f"{base_path}/{fname}")
            data = json.load(file)
            if len(data) > 0:
                scans += data
    return scans
        

def get_old_stats_json(base_path):
    stats = {}
    for stat_path in glob.glob(f"{base_path}/**/stat.json", recursive=True):
        with open(stat_path, "r") as file:
            old_stat = json.load(file)
            stats[stat_path] = old_stat
    return stats

def modify_stat_single(path, stat, sonar_scans):
    for fname in stat.keys():
        if fname == 'total' or fname == 'sales.c' or fname == 'temp.c' or fname == 'non_parsed':
            continue
        total_file_path = path.replace("stat.json", f"orig_output/{fname}") 
        stat[fname]["sonar"] = not (total_file_path in sonar_scans) if (not ".c" in fname and not "cwe-327/2-py" in path) else None # sonar does not scan .c files, and always identifies cwe-327 as insecure, so we ignore these cases
        stat[fname]["codeql"] = stat[fname]["sec"] if "sec" in stat[fname].keys() else None # if sec exists, then set codeql to its value, otherwise None
        stat[fname]["sec"] = (stat[fname]["sonar"] in [None, True]) and (stat[fname]["codeql"] in [None, True]) # and the two values together
        # sanity checks
        assert not ((stat[fname]["sonar"] == None) and (stat[fname]["codeql"] == None)) # code must have been scanned
        if False in [stat[fname]["sonar"], stat[fname]["codeql"]]:
            assert stat[fname]["sec"] == False 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--scans_dir", required=True)

    args = parser.parse_args()
    args.input = os.path.abspath(args.input)
    args.output = os.path.abspath(args.output)

    base_path = args.scans_dir
    sonar_vuln_files = get_sonar_scans(base_path)
    stats = get_old_stats_json(args.input)

    for path, stat in tqdm(stats.items()):

        modify_stat_single(path, stat, sonar_vuln_files)

        output_path = Path(path.replace(args.input, args.output).replace("stat.json", "new_stat.json"))
        # sanity checks
        assert not "/stat.json" in str(output_path.resolve())

        output_path.parents[0].mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as file:
            json.dump(stat, file, indent=4)


if __name__ == "__main__":
    main()    