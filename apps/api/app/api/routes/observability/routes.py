from fastapi import APIRouter

router = APIRouter(prefix="/observability", tags=["observability"])

_LINKS = [
    {"id": "obs1", "service_id": "svc2", "environment_id": "env1", "kind": "logs", "url": "http://example.local/logs"},
    {"id": "obs2", "service_id": "svc2", "environment_id": "env1", "kind": "metrics", "url": "http://example.local/metrics"},
]

@router.get("/links")
def list_links():
    return _LINKS
