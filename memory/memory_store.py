import json
import os

MEMORY_FILE = os.path.expanduser("~/.ai_coding_agent_memory.json")


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def add_memory(entry):

    memory = load_memory()

    memory.append(entry)

    save_memory(memory)


def search_memory(query):

    memory = load_memory()

    results = []

    for item in memory:
        if query.lower() in item["task"].lower():
            results.append(item)

    return results