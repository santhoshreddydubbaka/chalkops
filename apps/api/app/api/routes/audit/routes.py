from fastapi import APIRouter

router = APIRouter(prefix="/audit", tags=["audit"])

_EVENTS = [
    {"id": "e1", "action": "SYSTEM_BOOT", "actor": "system", "resource": "api", "ts": "demo"},
]

@router.get("/events")
def list_events():
    return _EVENTS
