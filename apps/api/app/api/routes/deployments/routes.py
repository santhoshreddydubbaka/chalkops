from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/deployments", tags=["deployments"])

_DEPLOYMENTS = []

class DeploymentCreate(BaseModel):
    service_id: str
    environment_id: str
    git_ref: str = "main"

@router.get("")
def list_deployments():
    return _DEPLOYMENTS

@router.post("")
def record_deployment(payload: DeploymentCreate):
    item = {
        "id": f"d{len(_DEPLOYMENTS)+1}",
        "service_id": payload.service_id,
        "environment_id": payload.environment_id,
        "git_ref": payload.git_ref,
        "status": "RECORDED",
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    _DEPLOYMENTS.append(item)
    return item

@router.post("/{deployment_id}/trigger")
def trigger_deployment(deployment_id: str):
    for d in _DEPLOYMENTS:
        if d["id"] == deployment_id:
            d["status"] = "TRIGGERED"
            d["triggered_at"] = datetime.utcnow().isoformat() + "Z"
            return d
    return {"error": "deployment not found"}
