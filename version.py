import json
import yaml
import sys

PACKAGE_JSON_FILE_PATH = "package.json"
CITATION_FILE_PATH = "CITATION.cff"
MASTER_VERSION_FILE = "VERSION"

def check():
    """
    Intended for use in CI pipelines, checks versions in files and exits with non-zero exit code if they don't match.
    """

    with open(PACKAGE_JSON_FILE_PATH, "r") as f:
        package_json = json.load(f)

    js_version = package_json['version']
    print(f"package.json version is {js_version}")

    with open(CITATION_FILE_PATH, "r") as f:
        citation_file = yaml.safe_load(f)

    citation_version = citation_file['version']
    print(f"CITATION.cff version is {citation_version}")

    master_version = get_master_version()
    print(f"VERSION file version is {master_version}")

    if js_version != master_version or citation_version != master_version:
        print("One or more versions does not match")
        sys.exit(1)
    else:
        print("All versions match!")

def get_master_version():
    with open(MASTER_VERSION_FILE, "r") as f:
            master_version = f.readline().strip()
    return master_version

def update():
    """
    Updates all versions to match the master version file.
    """
    master_version = get_master_version()
    
    with open(PACKAGE_JSON_FILE_PATH, "r") as f:
        package_json = json.load(f)
    print(f"Writing master version {master_version} to {PACKAGE_JSON_FILE_PATH}")
    with open(PACKAGE_JSON_FILE_PATH, "w") as f:
        package_json['version'] = master_version
        json.dump(package_json, f, indent=2)

    with open(CITATION_FILE_PATH, "r") as f:
        citation_file = yaml.safe_load(f)
    print(f"Writing master version {master_version} to {CITATION_FILE_PATH}")
    with open(CITATION_FILE_PATH, "w") as f:
        citation_file['version'] = master_version
        yaml.dump(citation_file, f)

    check()

if __name__ == "__main__":
    if sys.argv[1] == 'check':
        print("Checking versions...")
        check()
    elif sys.argv[1] == 'update':
        print("Updating versions...")
        update()
    else:
        print(f"Unknown function {sys.argv[1]}, available functions are 'check' and 'update'.")
