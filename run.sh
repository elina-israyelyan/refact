#!/usr/bin/env bash
set -e

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

 PYTHONPATH=src uvicorn src.main:app --reload --host 0.0.0.0 --port 8000