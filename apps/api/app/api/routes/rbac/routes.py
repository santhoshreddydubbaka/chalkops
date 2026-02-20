from fastapi import APIRouter, HTTPException
import psycopg

from app.config import settings

router = APIRouter(prefix="/rbac", tags=["rbac"])

def db_url() -> str:
    url = settings.database_url
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL missing. Set it in apps/api/.env")
    return url

@router.get("/roles")
def list_roles():
    with psycopg.connect(db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("select id, name from roles order by id;")
            rows = cur.fetchall()
    return [{"id": r[0], "name": r[1]} for r in rows]

@router.get("/users")
def list_users():
    with psycopg.connect(db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                select u.id, u.email, array_remove(array_agg(ur.role_id), null) as roles
                from users u
                left join user_roles ur on ur.user_id = u.id
                group by u.id, u.email
                order by u.id;
            """)
            rows = cur.fetchall()

    return [{"id": r[0], "email": r[1], "roles": r[2]} for r in rows]