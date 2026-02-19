from fastapi import APIRouter

router = APIRouter(prefix="/runbooks", tags=["runbooks"])

_RUNBOOKS = [
    {"id": "rb1", "title": "API down (local)", "steps": ["Check /health", "Check logs", "Restart uvicorn"]},
    {"id": "rb2", "title": "Frontend not loading (local)", "steps": ["Check vite terminal", "Restart npm run dev"]},
]

@router.get("")
def list_runbooks():
    return _RUNBOOKS
