# MiniVault API

A lightweight, local-first REST API simulating a core ModelVault feature: running a local LLM to respond to a prompt — fully offline.

**Author**: Do Minh Long (`skydev1031@gmail.com`)

---

## Features

- `POST /generate` endpoint powered by a local LLM (via [Ollama](https://ollama.com))
- Logs each interaction to `logs/log.jsonl`
- Command-line tool: `minivault --prompt "..."` or `--status`
- `/status` endpoint reports memory + uptime
- Docker support
- Packaged with `pyproject.toml` for CLI installation

---

## Requirements

- Python 3.10+
- Ollama running locally (e.g., `ollama run llama3`)

---

## Setup & Run

### ⬇Install dependencies

```bash
pip install -r requirements.txt
uvicorn minivault.main:app --reload

## Run Methods
1. Run without packaging (just scripts)
    python minivault/cli.py --prompt "Hello, who are you?"
    python minivault/cli.py --status

2. Run after packaging (via pip install -e .)
    pip install -e .
    minivault --prompt "Hello, who are you?"
    minivault --status

3. Run with Docker
    docker build -t minivault .
    docker run -p 8000:8000 minivault
