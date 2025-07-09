#!/usr/bin/env bash
set -e

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
export LLM_CLIENT_TYPE=mock
export WIKI_CLIENT_TYPE=mock
export GEMINI_SA_CREDENTIAL_PATH=path/to/your/credentials.json
PYTHONPATH=src uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-level info