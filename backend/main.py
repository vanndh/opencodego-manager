"""FastAPI entrypoint.

- /api/*  — REST для UI
- /ws     — WebSocket hub (PHASE 4 stub, наполнение в след. фазах)
- /       — статика собранного frontend (frontend/dist)
"""

import threading
import webbrowser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api import accounts, system
from config import app as cfg
from security import vault
from storage.db import init_db

app = FastAPI(title=cfg.APP_NAME, version=cfg.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system.router)
app.include_router(accounts.router)


@app.on_event("startup")
async def _startup():
    await init_db()
    vault.unlock()


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
