import subprocess
import argparse
from pathlib import Path
import requests
import json
from time import sleep

PROJECT_KEY = "secure_code_gen"

def new_project(admin_token=None, project_key=PROJECT_KEY, host_url="http://localhost:9000"):
    """
    """

    url = f"{host_url}/api/projects/create"
    params = {
        "name":project_key, 
        "project":project_key, 
        }
    headers = {
        "Authorization":f"Bearer {admin_token}"
    }

    requests.post(url, params, headers=headers)

    return project_key

def scan_path(path, admin_token=None, project_key=PROJECT_KEY, host_url="http://127.0.0.1:9000"):
    """
    scan the given path with the given project key
    the project must already exist
    """

    url = f"{host_url}/api/project_analyses/search"
    params = {
        "project":project_key, 
        }
    headers = {
        "Authorization":f"Bearer {admin_token}"
    }
    #print(headers)
    #print(requests.get(url, params, headers=headers).text)
    prev_num_analyses = len(requests.get(url, params, headers=headers).json()["analyses"])

    command = [
        ".sonar/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner", 
        f"-Dsonar.token={admin_token}",
        f"-Dsonar.projectKey={project_key}", 
        f"-Dsonar.projectBaseDir={path}",
        f"-Dsonar.sources={path}", 
        f"-Dsonar.host.url={host_url}",
        f"-Dsonar.inclusions=**/orig_output/*.py",
        "-Dsonar.scm.exclusions.disabled=true",
        "-X"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stdout.decode())
        print(result.stderr.decode())
    assert result.returncode == 0

    with open("logs.txt", "a") as file:
        file.write("\n\n\n" + str(path) + "\n" +result.stdout.decode())
        
    retries = 6
    while(len(requests.get(url, params, headers=headers).json()["analyses"]) == prev_num_analyses) and retries < 0:
        #print("waiting...")
        sleep(10)
        retries -= 1


def get_insecure_files(admin_token=None, project_key=PROJECT_KEY, issue_levels=["LOW", "MEDIUM", "HIGH"], host_url="http://localhost:9000"):
    """
    returns a list of insecure files given the project key
    the project must have already been scanned
    """

    files = []
    url = f"{host_url}/api/measures/component_tree"
    params = {
        "component":project_key, 
        "metricKeys":["security_issues"], 
        "qualifiers":["FIL"],
        "ps":500,
        "p":1
        }
    headers = {
        "Authorization":f"Bearer {admin_token}"
    }
    #print(
    total_pages = 2

    while params["p"] < total_pages:
        try:
            response = requests.get(url, params, headers=headers)
            tree = response.json()
            with open("api_logs.txt", "a") as file:
                file.write("\n\n" + str(tree))
            total_pages = 1 + tree["paging"]["total"] // params["ps"]
            for component in tree["components"]:
                sec_issues = json.loads(component["measures"][0]["value"])
                if True in [(sec_issues[issue_level] > 0) for issue_level in issue_levels]:
                    files.append(component["path"])
            params["p"] += 1
        except Exception as e:
            print(e)
            sleep(10)
        
    return files

def complete_scan(path, admin_token):
    print("generating sonar project...")
    new_project(admin_token=admin_token)
    print("scanning project...")
    scan_path(path, admin_token=admin_token)
    print("finding vulnerable files...")
    return get_insecure_files(admin_token=admin_token)

    
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--admin_token", type=str, required=True)
    parser.add_argument("--path", type=str, required=True)

    #admin_token = "squ_d40131dac58197cee581d64dd1dbeb24e6413af5"

    args = parser.parse_args()

    complete_scan(args.path, args.admin_token)

if __name__ == "__main__":
    main()
