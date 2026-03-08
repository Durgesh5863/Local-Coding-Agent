import os

CODE_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".go",
    ".rs"
)


def scan_repo(repo_path):

    files = []

    for root, dirs, filenames in os.walk(repo_path):

        for file in filenames:

            if file.endswith(CODE_EXTENSIONS):

                path = os.path.join(root, file)

                try:
                    with open(path, "r", errors="ignore") as f:
                        content = f.read()

                    files.append({
                        "path": path,
                        "content": content
                    })

                except:
                    pass

    return files