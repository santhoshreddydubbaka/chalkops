from fastapi import APIRouter

router = APIRouter(prefix="/services", tags=["services"])

_SERVICES = [
    {"id": "svc1", "name": "frontend", "type": "vercel", "owner": "platform"},
    {"id": "svc2", "name": "api", "type": "fastapi", "owner": "platform"},
]

@router.get("")
def list_services():
    return _SERVICES
