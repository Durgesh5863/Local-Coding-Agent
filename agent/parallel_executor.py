from concurrent.futures import ThreadPoolExecutor, as_completed
import re

from agent.retriever import retrieve_files
from agent.file_selector import select_files
from agent.planner import create_plan
from agent.coder import generate_code
from agent.tester import run_tests
from agent.memory_agent import recall_memory

from utils.diff_utils import show_diff, apply_patch
from memory.memory_store import add_memory


def execute_step(repo, step):

    print(f"\n[Agent] Executing step: {step}\n")

    memory_context = recall_memory(step)

    files = retrieve_files(repo, step)

    selected_files = select_files(step, files)

    if not selected_files:
        selected_files = files

    plan = create_plan(step + "\n" + memory_context, selected_files)

    print("\nPlan:\n", plan)

    response = generate_code(step, plan, selected_files)

    matches = re.findall(
        r"FILE:\s*(.*?)\nNEW_CODE:\n([\s\S]*?)(?=\nFILE:|\Z)",
        response
    )

    for file_path, new_code in matches:

        try:

            with open(file_path, "r") as f:
                old_code = f.read()

            print("\nDiff for:", file_path)

            show_diff(old_code, new_code)

            apply_patch(file_path, new_code)

        except FileNotFoundError:
            print("File not found:", file_path)

    test_output = run_tests()

    print("\nTest Results:\n", test_output)

    add_memory({
        "task": step,
        "solution": plan
    })

    return step


def run_parallel(repo, steps):

    print("\nRunning agents in parallel...\n")

    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = [
            executor.submit(execute_step, repo, step)
            for step in steps
        ]

        for future in as_completed(futures):

            print("\nCompleted:", future.result())