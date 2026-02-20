from fastapi import APIRouter, HTTPException
import psycopg

from app.config import settings

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/events")
def list_events():
    url = settings.database_url
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL missing. Set it in apps/api/.env")

    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                select id, action, actor, resource, ts
                from audit_events
                order by ts desc;
            """)
            rows = cur.fetchall()

    return [
        {"id": r[0], "action": r[1], "actor": r[2], "resource": r[3], "ts": r[4].isoformat()}
        for r in rows
    ]