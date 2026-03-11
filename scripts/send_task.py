import sys
import os
import requests

task = sys.argv[1]

repo = os.getcwd()

url = "http://localhost:8000/task"

params = {
    "task": task,
    "repo": repo
}

r = requests.get(url, params=params)

print(r.text)