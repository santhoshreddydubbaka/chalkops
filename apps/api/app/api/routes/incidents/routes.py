from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/incidents", tags=["incidents"])

_INCIDENTS = []

class IncidentCreate(BaseModel):
    title: str
    severity: str = "SEV3"
    service_id: str
    environment_id: str

@router.get("")
def list_incidents():
    return _INCIDENTS

@router.post("")
def create_incident(payload: IncidentCreate):
    item = {
        "id": f"inc{len(_INCIDENTS)+1}",
        "title": payload.title,
        "severity": payload.severity,
        "status": "OPEN",
        "service_id": payload.service_id,
        "environment_id": payload.environment_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    _INCIDENTS.append(item)
    return item

@router.post("/{incident_id}/close")
def close_incident(incident_id: str):
    for inc in _INCIDENTS:
        if inc["id"] == incident_id:
            inc["status"] = "CLOSED"
            inc["closed_at"] = datetime.utcnow().isoformat() + "Z"
            return inc
    return {"error": "incident not found"}
