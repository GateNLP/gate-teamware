import json
import yaml
import re
import sys

PACKAGE_JSON_FILE_PATH = "package.json"
DOCS_PACKAGE_JSON_FILE_PATH = "docs/package.json"
CITATION_FILE_PATH = "CITATION.cff"
MASTER_VERSION_FILE = "VERSION"
README_FILE_PATH = "README.md"

def check():
    """
    Intended for use in CI pipelines, checks versions in files and exits with non-zero exit code if they don't match.
    """

    js_version = get_package_json_version(PACKAGE_JSON_FILE_PATH)
    print(f"package.json version is {js_version}")

    docs_js_version = get_package_json_version(DOCS_PACKAGE_JSON_FILE_PATH)
    print(f"docs package.json version is {docs_js_version}")

    with open(CITATION_FILE_PATH, "r") as f:
        citation_file = yaml.safe_load(f)

    citation_version = citation_file['version']
    print(f"{CITATION_FILE_PATH} version is {citation_version}")

    readme_version = get_readme_version(README_FILE_PATH)
    print(f"{README_FILE_PATH} version is {readme_version}")

    master_version = get_master_version()
    print(f"VERSION file version is {master_version}")

    if js_version != master_version or docs_js_version != master_version or citation_version != master_version or readme_version != master_version:
        print("One or more versions does not match")
        sys.exit(1)
    else:
        print("All versions match!")

def get_package_json_version(file_path: str) -> str:
    with open(file_path, "r") as f:
        package_json = json.load(f)

    js_version = package_json['version']
    return js_version

def get_readme_version(file_path: str) -> str:
    with open(file_path, 'r') as f:
        readme_text = f.read()
    
    match = re.search(r'\(Version (.*)\)', readme_text)

    if match is None:
        print(f"No version found in {README_FILE_PATH}.")
        return
    elif len(match.groups()) > 1:
        print(f"{len(match.groups())} matches found in {README_FILE_PATH}, expected 1.")
        return
    else:
        return match.groups(1)[0]

def get_master_version():
    with open(MASTER_VERSION_FILE, "r") as f:
            master_version = f.readline().strip()
    return master_version

def update():
    """
    Updates all versions to match the master version file.
    """
    master_version = get_master_version()

    update_package_json_version(PACKAGE_JSON_FILE_PATH, master_version)

    update_package_json_version(DOCS_PACKAGE_JSON_FILE_PATH, master_version)

    update_readme_version(README_FILE_PATH, master_version)

    with open(CITATION_FILE_PATH, "r") as f:
        citation_file = yaml.safe_load(f)
    print(f"Writing master version {master_version} to {CITATION_FILE_PATH}")
    with open(CITATION_FILE_PATH, "w") as f:
        citation_file['version'] = master_version
        yaml.dump(citation_file, f)

    check()

def update_package_json_version(file_path:str, version_no:str):
    with open(file_path, "r") as f:
        package_json = json.load(f)
    print(f"Writing master version {version_no} to {file_path}")
    with open(file_path, "w") as f:
        package_json['version'] = version_no
        json.dump(package_json, f, indent=2)

def update_readme_version(file_path:str, version_no:str):
    with open(file_path, 'r') as f:
        readme_text = f.read()
    
    readme_text = re.sub(
           r'\(Version (.*)\)', 
           f'(Version {version_no})', 
           readme_text
       )

    with open(file_path, 'w') as f:
        f.write(readme_text)


if __name__ == "__main__":
    if sys.argv[1] == 'check':
        print("Checking versions...")
        check()
    elif sys.argv[1] == 'update':
        print("Updating versions...")
        update()
    else:
        print(f"Unknown function {sys.argv[1]}, available functions are 'check' and 'update'.")
