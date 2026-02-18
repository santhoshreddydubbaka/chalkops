from fastapi import APIRouter

router = APIRouter(prefix="/rbac", tags=["rbac"])

@router.get("/roles")
def list_roles():
    # placeholder until DB is added
    return [{"id": "admin", "name": "Admin"}, {"id": "viewer", "name": "Viewer"}]

@router.get("/users")
def list_users():
    # placeholder until DB is added
    return [{"id": "u1", "email": "demo@chalkops.local", "roles": ["admin"]}]
