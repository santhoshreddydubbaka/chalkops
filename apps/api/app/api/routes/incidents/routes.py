from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg

from app.config import settings

router = APIRouter(prefix="/incidents", tags=["incidents"])

class IncidentCreate(BaseModel):
    title: str
    severity: str = "SEV3"
    service_id: str
    environment_id: str

def db_url() -> str:
    url = settings.database_url
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL missing. Set it in apps/api/.env")
    return url

@router.get("")
def list_incidents():
    with psycopg.connect(db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                select id, title, severity, status, service_id, environment_id, created_at, closed_at
                from incidents
                order by created_at desc;
            """)
            rows = cur.fetchall()

    return [
        {
            "id": r[0],
            "title": r[1],
            "severity": r[2],
            "status": r[3],
            "service_id": r[4],
            "environment_id": r[5],
            "created_at": r[6].isoformat(),
            "closed_at": r[7].isoformat() if r[7] else None,
        }
        for r in rows
    ]

@router.post("")
def create_incident(payload: IncidentCreate):
    with psycopg.connect(db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("select count(*) from incidents;")
            n = cur.fetchone()[0]
            new_id = f"inc{n+1}"

            cur.execute("""
                insert into incidents (id, title, severity, status, service_id, environment_id)
                values (%s, %s, %s, 'OPEN', %s, %s)
                returning id, title, severity, status, service_id, environment_id, created_at, closed_at;
            """, (new_id, payload.title, payload.severity, payload.service_id, payload.environment_id))
            row = cur.fetchone()
        conn.commit()

    return {
        "id": row[0],
        "title": row[1],
        "severity": row[2],
        "status": row[3],
        "service_id": row[4],
        "environment_id": row[5],
        "created_at": row[6].isoformat(),
        "closed_at": row[7].isoformat() if row[7] else None,
    }

@router.post("/{incident_id}/close")
def close_incident(incident_id: str):
    with psycopg.connect(db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                update incidents
                set status='CLOSED', closed_at=now()
                where id=%s
                returning id, title, severity, status, service_id, environment_id, created_at, closed_at;
            """, (incident_id,))
            row = cur.fetchone()
        conn.commit()

    if not row:
        raise HTTPException(status_code=404, detail="incident not found")

    return {
        "id": row[0],
        "title": row[1],
        "severity": row[2],
        "status": row[3],
        "service_id": row[4],
        "environment_id": row[5],
        "created_at": row[6].isoformat(),
        "closed_at": row[7].isoformat() if row[7] else None,
    }