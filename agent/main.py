import os
import re

from agent.retriever import retrieve_files
from agent.planner import create_plan
from agent.coder import generate_code
from agent.tester import run_tests
from agent.indexer import index_repo
from utils.diff_utils import show_diff, apply_patch


def run_agent(task):

    repo = os.getcwd()

    print("\nIndexing repository...\n")
    index_repo(repo)

    print("\nRetrieving relevant files...\n")
    files = retrieve_files(repo, task)

    print("\nPlanning solution...\n")
    plan = create_plan(task, files)

    print(plan)

    print("\nGenerating code changes...\n")
    response = generate_code(task, plan, files)

    print(response)

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

    print("\nRunning tests...\n")

    test_output = run_tests()

    print(test_output)