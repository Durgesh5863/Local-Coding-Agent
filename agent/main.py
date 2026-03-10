import os

from agent.indexer import index_repo
from agent.task_decomposer import decompose_task
from agent.parallel_executor import run_parallel


def run_agent(task):

    repo = os.getcwd()

    print("\n=================================")
    print("        AI CODING AGENT")
    print("=================================\n")

    print("Repository:", repo)

    # ---------------------------------------
    # 1. Decompose task
    # ---------------------------------------

    print("\nDecomposing task...\n")

    steps = decompose_task(task)

    if not steps:
        steps = [task]

    for i, step in enumerate(steps, start=1):
        print(f"{i}. {step}")

    # ---------------------------------------
    # 2. Index repo
    # ---------------------------------------

    print("\nIndexing repository...\n")

    index_repo(repo)

    # ---------------------------------------
    # 3. Execute steps in parallel
    # ---------------------------------------

    print("\nLaunching parallel coding agents...\n")

    run_parallel(repo, steps)

    print("\n=================================")
    print("Agent execution completed.")
    print("=================================\n")