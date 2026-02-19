from fastapi import APIRouter, HTTPException
import psycopg

from app.config import settings

router = APIRouter(prefix="/observability", tags=["observability"])

@router.get("/links")
def list_links():
    url = settings.database_url
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL missing. Set it in apps/api/.env")

    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                select id, service_id, environment_id, kind, url
                from observability_links
                order by id;
            """)
            rows = cur.fetchall()

    return [
        {"id": r[0], "service_id": r[1], "environment_id": r[2], "kind": r[3], "url": r[4]}
        for r in rows
    ]