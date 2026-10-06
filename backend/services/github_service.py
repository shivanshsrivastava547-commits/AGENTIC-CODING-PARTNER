import os
import shutil
from git import Repo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.join(BASE_DIR, "repos")

os.makedirs(REPO_DIR, exist_ok=True)

def clone_repo(repo_url: str):
    # delete all previously cloned repos
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR, ignore_errors=True)

    os.makedirs(REPO_DIR, exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = os.path.join(REPO_DIR, repo_name)

    print("Cloning fresh repo into:", local_path)

    Repo.clone_from(
        repo_url,
        local_path,
        depth=1
    )

    return local_path