from utils.ollama_client import generate


def select_files(task, files):

    file_list = "\n".join([f["path"] for f in files])

    prompt = f"""
You are a software architect.

Task:
{task}

Available files:
{file_list}

Select the most relevant files to modify.
Return only file paths.
"""

    response = generate(prompt)

    selected = []

    for f in files:
        if f["path"] in response:
            selected.append(f)

    return selected