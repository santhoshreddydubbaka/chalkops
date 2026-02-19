from fastapi import APIRouter, HTTPException
import psycopg

from app.config import settings

router = APIRouter(prefix="/runbooks", tags=["runbooks"])

@router.get("")
def list_runbooks():
    url = settings.database_url
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL missing. Set it in apps/api/.env")

    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("select id, title, steps from runbooks order by id;")
            rows = cur.fetchall()

    return [{"id": r[0], "title": r[1], "steps": r[2]} for r in rows]