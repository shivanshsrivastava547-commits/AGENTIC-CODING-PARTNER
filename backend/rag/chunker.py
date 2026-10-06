import os

SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".html",
    ".css",
]

IGNORE_DIRS = [
    "node_modules",
    ".git",
    "venv",
    "__pycache__",
    ".next",
    "dist",
    "build",
    ".vscode",
]

IGNORE_FILES = [
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "requirements.txt",
    "Pipfile.lock",
]

def read_repo_files(repo_path):
    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
        ]

        for file in files:

            # Skip unwanted files
            if file in IGNORE_FILES:
                continue

            ext = os.path.splitext(file)[1]

            # Skip unsupported extensions
            if ext not in SUPPORTED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            try:
                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:
                    content = f.read()

                if not content.strip():
                    continue

                documents.append({
                    "content": content,
                    "metadata": {
                        "source": os.path.relpath(
                            file_path,
                            repo_path
                        ),
                        "file_name": file,
                        "extension": ext,
                    }
                })

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    print(f"Files indexed: {len(documents)}")

    return documents