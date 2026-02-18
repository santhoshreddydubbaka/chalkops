# ChalkOps API (FastAPI) — Local Run

## What it is
FastAPI backend that serves REST endpoints for the React frontend.

## Run locally
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi "uvicorn[standard]"
uvicorn main:app --reload --port 8000

Test:
http://127.0.0.1:8000/health
Docs:
http://127.0.0.1:8000/docs
