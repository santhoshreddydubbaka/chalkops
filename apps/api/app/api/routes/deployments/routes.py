from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg

from app.config import settings

router = APIRouter(prefix="/deployments", tags=["deployments"])

class DeploymentCreate(BaseModel):
    service_id: str
    environment_id: str
    git_ref: str = "main"

def db_url() -> str:
    url = settings.database_url
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL missing. Set it in apps/api/.env")
    return url

@router.get("")
def list_deployments():
    with psycopg.connect(db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                select id, service_id, environment_id, git_ref, status,
                       created_at, triggered_at
                from deployments
                order by created_at desc;
            """)
            rows = cur.fetchall()

    def row_to_dict(r):
        return {
            "id": r[0],
            "service_id": r[1],
            "environment_id": r[2],
            "git_ref": r[3],
            "status": r[4],
            "created_at": r[5].isoformat(),
            "triggered_at": r[6].isoformat() if r[6] else None,
        }

    return [row_to_dict(r) for r in rows]

@router.post("")
def record_deployment(payload: DeploymentCreate):
    with psycopg.connect(db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("select count(*) from deployments;")
            n = cur.fetchone()[0]
            new_id = f"d{n+1}"

            cur.execute("""
                insert into deployments (id, service_id, environment_id, git_ref, status)
                values (%s, %s, %s, %s, %s)
                returning id, service_id, environment_id, git_ref, status, created_at, triggered_at;
            """, (new_id, payload.service_id, payload.environment_id, payload.git_ref, "RECORDED"))
            row = cur.fetchone()
        conn.commit()

    return {
        "id": row[0],
        "service_id": row[1],
        "environment_id": row[2],
        "git_ref": row[3],
        "status": row[4],
        "created_at": row[5].isoformat(),
        "triggered_at": row[6].isoformat() if row[6] else None,
    }

@router.post("/{deployment_id}/trigger")
def trigger_deployment(deployment_id: str):
    with psycopg.connect(db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                update deployments
                set status = 'TRIGGERED', triggered_at = now()
                where id = %s
                returning id, service_id, environment_id, git_ref, status, created_at, triggered_at;
            """, (deployment_id,))
            row = cur.fetchone()
        conn.commit()

    if not row:
        raise HTTPException(status_code=404, detail="deployment not found")

    return {
        "id": row[0],
        "service_id": row[1],
        "environment_id": row[2],
        "git_ref": row[3],
        "status": row[4],
        "created_at": row[5].isoformat(),
        "triggered_at": row[6].isoformat() if row[6] else None,
    }