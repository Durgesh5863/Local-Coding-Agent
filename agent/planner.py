from utils.ollama_client import generate


def create_plan(task, files):

    file_list = "\n".join([f["path"] for f in files])

    prompt = f"""
You are a senior software architect.

Task:
{task}

Relevant files:
{file_list}

Create a step-by-step plan to solve the task.
Explain which files should be modified and why.
"""

    response = generate(prompt)

    return response