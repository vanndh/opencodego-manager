"""FastAPI entrypoint.

- /api/*  — REST для UI
- /ws     — WebSocket hub (realtime события)
- /gateway — отдельный локальный API (поднимается опционально)
- /       — статика собранного frontend (frontend/dist)
"""

import threading
import webbrowser

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api import accounts, bonuses, creds, gateway, system
from config import app as cfg
from core.ws_hub import hub
from security import vault
from storage.db import get_session, init_db
from workers.registry import WorkerRegistry

app = FastAPI(title=cfg.APP_NAME, version=cfg.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system.router)
app.include_router(accounts.router)
app.include_router(bonuses.router)
app.include_router(creds.router)
app.include_router(gateway.router)

registry = WorkerRegistry()


@app.on_event("startup")
async def _startup():
    await init_db()
    vault.unlock()
    registry.set_session_factory(get_session)


@app.on_event("shutdown")
async def _shutdown():
    await registry.stop_all()


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket, since: int = 0):
    await hub.connect(ws, since=since)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        hub.disconnect(ws)


@app.get("/")
async def index():
    index = cfg.FRONTEND_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"status": "frontend not built — run: cd frontend && npm run build"}


def _open_browser():
    webbrowser.open(f"http://{cfg.API_HOST}:{cfg.API_PORT}/")


def main():
    import uvicorn

    if cfg.LAUNCH_BROWSER:
        threading.Timer(1.0, _open_browser).start()

    uvicorn.run(app, host=cfg.API_HOST, port=cfg.API_PORT, log_level="info")


if __name__ == "__main__":
    main()
