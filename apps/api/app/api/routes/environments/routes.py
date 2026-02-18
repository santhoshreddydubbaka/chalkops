from fastapi import APIRouter

router = APIRouter(prefix="/environments", tags=["environments"])

_ENVIRONMENTS = [
    {"id": "env1", "name": "dev", "service_id": "svc2", "url": "http://127.0.0.1:8000"},
    {"id": "env2", "name": "local-web", "service_id": "svc1", "url": "http://localhost:5173"},
]

@router.get("")
def list_environments():
    return _ENVIRONMENTS
