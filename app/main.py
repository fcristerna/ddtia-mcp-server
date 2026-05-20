import contextlib
import logging
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware as StarletteCORSMiddleware

from app.clients.sonoras.db import init_db
from app.mcp.server import mcp as _mcp
from app.routes.health import router as health_router
from app.routes.webhooks import router as webhooks_router
from app.routes.tools import router as tools_router
from app.routes.sonoras import router as sonoras_router

# ─── Logging ────────────────────────────────────────────────────────────────
LOG_FILE = os.getenv("LOG_FILE", "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE),
    ]
)
log = logging.getLogger(__name__)

# ─── MCP Setup ───────────────────────────────────────────────────────────────
# Routes exposed:
#   POST /mcp   — Streamable HTTP (primary, configure this URL in GHL)
#   GET  /sse   — SSE stream (fallback)
#   POST /messages/ — SSE message endpoint
_http_app = _mcp.streamable_http_app()
_sse_app = _mcp.sse_app()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    async with _mcp.session_manager.run():
        log.info("MCP session manager started")
        yield
    log.info("MCP session manager stopped")


# ─── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="GHL MCP - Calendario",
    description="Tools MCP para agendar citas desde AI Agent Studio",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sonorascarbonysal.com",
        "https://www.sonorascarbonysal.com",
        "https://claude.ai",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ─── Routers ─────────────────────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(webhooks_router)
app.include_router(tools_router)
app.include_router(sonoras_router)

# ─── MCP Mount ───────────────────────────────────────────────────────────────
# FastAPI routes above take precedence; this sub-app catches /mcp, /sse, /messages/
_CORS_ORIGINS = [
    "https://claude.ai",
    "https://sonorascarbonysal.com",
    "https://www.sonorascarbonysal.com",
]
app.mount("/", Starlette(
    routes=list(_http_app.routes) + list(_sse_app.routes),
    middleware=[Middleware(
        StarletteCORSMiddleware,
        allow_origins=_CORS_ORIGINS,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )],
))
