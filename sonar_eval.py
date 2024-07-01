import argparse
import os
import re
import json
from pathlib import Path
from tqdm import tqdm

import sonar_scan

def scan_paths(base_path, scans_dir, admin_token):

    all_vulns = []

    sonar_scan.new_project(admin_token=admin_token)

    paths = []
    for model in os.listdir(base_path):
        for seed in os.listdir(Path(base_path) / model):
            paths.append(Path(base_path) / model / seed)

    paths = list(filter(lambda p: os.path.isdir(p), paths))
    paths = list(filter(lambda p: not (".scannerwork" in str(p.resolve())), paths))
    existing_data = os.listdir(f"./{scans_dir}")
    paths = list(filter(lambda p: not (f"{str(p.resolve()).replace('/', '-')}.json" in existing_data), paths))

    for path in tqdm(paths):
        tqdm.write(str(path.resolve()))
        new_path = Path(base_path) / path
        sonar_scan.scan_path(new_path, admin_token=admin_token)
        vulns = sonar_scan.get_insecure_files(admin_token=admin_token)
        #tqdm.write(str(vulns))
        new_vulns = [str((new_path / vuln).resolve()) for vuln in vulns]
        tqdm.write(str(new_vulns)[:50])
        with open(f"./{scans_dir}/{str(path.resolve()).replace('/', '-')}.json", "w") as file:
            json.dump(new_vulns, file, indent=4)
        all_vulns += new_vulns
    
    return all_vulns

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--admin_token", type=str, default="squ_1b75841701601e8ccc0f9954f1f7a5e94d037b87")
    parser.add_argument("--path", type=str, default="experiments")
    parser.add_argument("--scans_dir", type=str, default="scans")

    args = parser.parse_args()
    args.path = os.path.abspath(args.path)

    if not os.path.exists(args.scans_dir):
        os.makedirs(args.scans_dir)

    with open("scan.json", "w") as file:
        scan_results = scan_paths(args.path, args.scans_dir, args.admin_token)
        json.dump(scan_results, file)

if __name__ == "__main__":
    main()
