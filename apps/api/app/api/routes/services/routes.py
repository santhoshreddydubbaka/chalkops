from fastapi import APIRouter, HTTPException
import psycopg

from app.config import settings

router = APIRouter(prefix="/services", tags=["services"])

@router.get("")
def list_services():
    url = settings.database_url
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL missing. Set it in apps/api/.env")

    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("select id, name, type, owner from services order by id;")
            rows = cur.fetchall()

    return [{"id": r[0], "name": r[1], "type": r[2], "owner": r[3]} for r in rows]
