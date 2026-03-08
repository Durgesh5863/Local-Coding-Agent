import typer
from agent.main import run_agent

app = typer.Typer()

@app.command()
def task(prompt: str):
    run_agent(prompt)

if __name__ == "__main__":
    app()