import os
import re

from agent.indexer import index_repo
from agent.retriever import retrieve_files
from agent.file_selector import select_files
from agent.planner import create_plan
from agent.coder import generate_code
from agent.tester import run_tests
from agent.memory_agent import recall_memory

from utils.diff_utils import show_diff, apply_patch
from memory.memory_store import add_memory


def run_agent(task):

    repo = os.getcwd()

    print("\n===== AI Coding Agent =====\n")

    print("Repository:", repo)

    # ---------------------------------------------------
    # 1. Recall previous memory
    # ---------------------------------------------------

    print("\nChecking memory for similar tasks...\n")

    memory_context = recall_memory(task)

    if memory_context:
        print(memory_context)

    # ---------------------------------------------------
    # 2. Index repository into Qdrant
    # ---------------------------------------------------

    print("\nIndexing repository...\n")

    index_repo(repo)

    # ---------------------------------------------------
    # 3. Retrieve relevant files
    # ---------------------------------------------------

    print("\nRetrieving relevant files...\n")

    files = retrieve_files(repo, task)

    print("Retrieved files:")

    for f in files:
        print(" -", f["path"])

    # ---------------------------------------------------
    # 4. File selection agent
    # ---------------------------------------------------

    print("\nSelecting most relevant files...\n")

    selected_files = select_files(task, files)

    for f in selected_files:
        print("Selected:", f["path"])

    # ---------------------------------------------------
    # 5. Planning
    # ---------------------------------------------------

    print("\nGenerating plan...\n")

    plan = create_plan(task + "\n" + memory_context, selected_files)

    print(plan)

    # ---------------------------------------------------
    # 6. Generate code edits
    # ---------------------------------------------------

    print("\nGenerating code modifications...\n")

    response = generate_code(task, plan, selected_files)

    print(response)

    # ---------------------------------------------------
    # 7. Parse generated patches
    # ---------------------------------------------------

    matches = re.findall(
        r"FILE:\s*(.*?)\nNEW_CODE:\n([\s\S]*?)(?=\nFILE:|\Z)",
        response
    )

    if not matches:
        print("\nNo code modifications proposed.\n")

    # ---------------------------------------------------
    # 8. Show diff and request approval
    # ---------------------------------------------------

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

    # ---------------------------------------------------
    # 9. Run tests
    # ---------------------------------------------------

    print("\nRunning tests...\n")

    test_output = run_tests()

    print(test_output)

    # ---------------------------------------------------
    # 10. Save solution to memory
    # ---------------------------------------------------

    print("\nSaving solution to memory...\n")

    add_memory({
        "task": task,
        "solution": plan
    })

    print("\nAgent execution completed.\n")