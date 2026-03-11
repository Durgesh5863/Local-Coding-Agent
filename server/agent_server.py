from fastapi import FastAPI
from agent.main import run_agent

app = FastAPI()


@app.get("/task")
def run_task(task: str):

    run_agent(task)

    return {"status": "completed", "task": task}