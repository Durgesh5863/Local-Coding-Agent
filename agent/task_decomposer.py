from utils.ollama_client import generate


def decompose_task(task):

    prompt = f"""
You are a senior software architect.

Break the following task into small executable steps.

Each step should be clear and focused.

Return steps as a numbered list.

Task:
{task}
"""

    response = generate(prompt)

    steps = []

    for line in response.split("\n"):
        line = line.strip()

        if line and line[0].isdigit():
            steps.append(line.split(".", 1)[1].strip())

    return steps