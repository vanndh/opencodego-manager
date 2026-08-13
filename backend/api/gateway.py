"""Роутер gateway — статус/start/stop/stats (ТЗ §34-36, §72).

Мок-статистика. Реальный proxy (localhost:3456) поднимается отдельным
sub-app'ом — фаза реализует конфигурацию и статус.
"""

from fastapi import APIRouter

from gateway.router import STRATEGY_MAP

router = APIRouter(prefix="/api/gateway", tags=["gateway"])

_state = {
    "running": False,
    "strategy": "most_available",
    "requests": 1248,
    "success": 1223,
    "errors": 25,
    "avg_latency_ms": 842,
    "switches": 114,
    "uptime_s": 0,
}


@router.get("")
async def gateway_status():
    return {
        "running": _state["running"],
        "endpoint": "http://127.0.0.1:3456",
        "strategies": list(STRATEGY_MAP.keys()),
        "strategy": _state["strategy"],
        "stats": {
            "requests": _state["requests"],
            "success": _state["success"],
            "errors": _state["errors"],
            "avg_latency_ms": _state["avg_latency_ms"],
            "switches": _state["switches"],
            "uptime_s": _state["uptime_s"],
        },
    }


@router.post("/start")
async def gateway_start():
    _state["running"] = True
    return {"ok": True, "running": True}


@router.post("/stop")
async def gateway_stop():
    _state["running"] = False
    return {"ok": True, "running": False}


@router.post("/strategy")
async def gateway_strategy(payload: dict):
    name = payload.get("strategy", "most_available")
    if name not in STRATEGY_MAP:
        return {"ok": False, "error": "unknown strategy"}
    _state["strategy"] = name
    return {"ok": True, "strategy": name}
