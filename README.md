We’ll install and configure:

Ollama

Qwen3.5 9B

Qdrant

your global coding agent

integration with Visual Studio Code + Continue

I’ll keep this clean and sequential so you can follow easily.

Step 1 — Install Ollama

Download and install Ollama.

Website:

https://ollama.com/download

Install normally.

Step 2 — Verify Ollama

Open terminal and run:

ollama --version

Then start the service:

ollama serve

Leave this terminal running.

Step 3 — Install Qwen3.5 9B Model

Pull the model:

ollama pull qwen3.5:9b

Test it:

ollama run qwen3.5:9b

Example prompt:

Explain quicksort in Python

If it replies → your local LLM works.

Install Continue extension.

Then go to C:\Users\Administrator\.continue

In the config.yaml,

name: Local Config
version: 1.0.0
schema: v1

models:
  - name: Qwen-3.5-9B
    provider: ollama
    model: qwen3.5:9b
    apiBase: http://localhost:11434

context:
  - provider: code
  - provider: folder
  - provider: terminal

experimental:
  agent: true

Add the above lines

ai-coding-agent/
│
├── agent/
│   │
│   ├── planner.py        # Planner agent: creates step-by-step plan
│   ├── retriever.py      # Retrieves relevant code from Qdrant
│   ├── coder.py          # Generates code changes
│   ├── tester.py         # Runs tests and captures errors
│   ├── indexer.py        # Indexes repo into Qdrant
│   ├── main.py           # Orchestrates all agents
│   │
│   └── __init__.py
│
├── embeddings/
│   └── embedder.py       # Embedding model loader (sentence-transformers)
│
├── utils/
│   ├── ollama_client.py  # Wrapper for Ollama API
│   ├── repo_utils.py     # Repo scanning helpers
│   └── diff_utils.py     # Show diffs before applying edits
│
├── config/
│   └── settings.py       # Global config (model name, qdrant host etc.)
│
├── scripts/
│   └── setup_index.py    # CLI script to index repo manually
│
├── code_agent_cli.py     # CLI entry point (code-agent command)
│
├── requirements.txt
│
└── README.md


How the Pipeline Works with This Structure

code_agent_cli.py
        │
        ▼
agent/main.py
        │
        ├── planner.py      → generate plan
        │
        ├── retriever.py    → query Qdrant for relevant files
        │
        ├── coder.py        → generate improved code
        │
        └── tester.py       → run tests + error feedback loop


Step 5 — Install Python Environment

Install required libraries.

pip install \
qdrant-client \
sentence-transformers \
requests \
rich \
typer

These will be used by your coding agent.

Step 6 — Start Qdrant (Vector Database)

Run using Docker:

docker run -p 6333:6333 qdrant/qdrant

Open browser:

http://localhost:6333/dashboard

Now your vector database is ready.