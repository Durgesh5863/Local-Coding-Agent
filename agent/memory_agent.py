from memory.memory_store import search_memory


def recall_memory(task):

    memories = search_memory(task)

    if not memories:
        return ""

    context = "\nPrevious similar fixes:\n"

    for m in memories:
        context += f"\nTask: {m['task']}\nSolution: {m['solution']}\n"

    return context