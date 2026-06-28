import os
import sys
from pathlib import Path


current_file = Path(__file__).resolve()
src_dir = current_file.parents[2]
sys.path.insert(0, str(src_dir))


from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from presentation.api.routers.archive_routes import archive_router


APP_MODE = os.getenv("APP_MODE", "dev")

app = FastAPI(
    title="EMIR LOCAL API",
    description="EMIR LOCAL API",
    version="0.1.4",
    deprecated=False,
    docs_url=None if APP_MODE == "production" else "/docs",
    redoc_url=None if APP_MODE == "production" else "/redoc",
    openapi_url=None if APP_MODE == "production" else "/openapi.json"
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["access-control-allow-headers"] = "authorization, content-type"
        response.headers["access-control-allow-methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        response.headers["access-control-allow-origin"] = os.getenv("CORS_ALLOW_ORIGIN", "")
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
app.add_middleware(SecurityHeadersMiddleware)

@app.options("/{path:path}")
async def options_handler(path: str):
    return Response(
        content="",
        headers={
            "access-control-allow-origin": os.getenv("CORS_ALLOW_ORIGIN", ""),
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
        },
        status_code=200
    )

@app.get("/")
def status_check():
    return {'status': 'ok'}

app.include_router(
    archive_router,
    prefix="/api/archive",
    tags=["Archive"],
    deprecated=False
)

# from infrastructure.persistence.sqlalchemy.config import Base, engine
# Base.metadata.create_all(engine)
