from utils.ollama_client import generate


def generate_code(task, plan, files):

    code_context = ""

    for f in files:
        code_context += f"\nFILE: {f['path']}\n{f['content']}\n"

    prompt = f"""
You are a senior software engineer.

Task:
{task}

Plan:
{plan}

Relevant code:
{code_context}

Return modifications in this format:

FILE: <file_path>
NEW_CODE:
<full updated file content>
"""

    response = generate(prompt)

    return response