import os
import re

from agent.indexer import index_repo
from agent.retriever import retrieve_files
from agent.file_selector import select_files
from agent.planner import create_plan
from agent.coder import generate_code
from agent.tester import run_tests
from agent.memory_agent import recall_memory
from agent.task_decomposer import decompose_task

from utils.diff_utils import show_diff, apply_patch
from memory.memory_store import add_memory


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
    # 3. Execute each step
    # ---------------------------------------

    for step in steps:

        print("\n=================================")
        print("Executing Step:", step)
        print("=================================\n")

        # ---------------------------------------
        # Memory recall
        # ---------------------------------------

        memory_context = recall_memory(step)

        if memory_context:
            print("\nRelevant memory found:\n")
            print(memory_context)

        # ---------------------------------------
        # Retrieve relevant files
        # ---------------------------------------

        print("\nRetrieving relevant files...\n")

        files = retrieve_files(repo, step)

        print("Retrieved files:")

        for f in files:
            print(" -", f["path"])

        # ---------------------------------------
        # File selection
        # ---------------------------------------

        print("\nSelecting most relevant files...\n")

        selected_files = select_files(step, files)

        for f in selected_files:
            print("Selected:", f["path"])

        if not selected_files:
            selected_files = files

        # ---------------------------------------
        # Planning
        # ---------------------------------------

        print("\nGenerating plan...\n")

        plan = create_plan(step + "\n" + memory_context, selected_files)

        print(plan)

        # ---------------------------------------
        # Code generation
        # ---------------------------------------

        print("\nGenerating code modifications...\n")

        response = generate_code(step, plan, selected_files)

        print(response)

        # ---------------------------------------
        # Parse patches
        # ---------------------------------------

        matches = re.findall(
            r"FILE:\s*(.*?)\nNEW_CODE:\n([\s\S]*?)(?=\nFILE:|\Z)",
            response
        )

        if not matches:
            print("\nNo code modifications proposed.\n")

        # ---------------------------------------
        # Diff preview + approval
        # ---------------------------------------

        for file_path, new_code in matches:

            try:

                with open(file_path, "r") as f:
                    old_code = f.read()

                print("\n----------------------------------")
                print("File:", file_path)
                print("----------------------------------\n")

                show_diff(old_code, new_code)

                apply_patch(file_path, new_code)

            except FileNotFoundError:
                print("File not found:", file_path)

        # ---------------------------------------
        # Run tests
        # ---------------------------------------

        print("\nRunning tests...\n")

        test_output = run_tests()

        print(test_output)

        # ---------------------------------------
        # Save memory
        # ---------------------------------------

        add_memory({
            "task": step,
            "solution": plan
        })

    print("\n=================================")
    print("Agent execution completed.")
    print("=================================\n")