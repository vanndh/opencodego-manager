"""WS hub — realtime события (ТЗ §17).

In-process event bus → single WS connection per tab.
Resume via last_event_id. Per-account debounce.
"""

import asyncio
import time
import uuid

from fastapi import WebSocket


class EventHub:
    def __init__(self):
        self._clients: list[WebSocket] = []
        self._last_event_id = 0
        self._history: list[dict] = []
        self._history_max = 500

    async def connect(self, ws: WebSocket, since: int = 0):
        await ws.accept()
        self._clients.append(ws)
        # дослать пропущенные события
        for ev in self._history:
            if ev["id"] > since:
                await ws.send_json(ev)

    def disconnect(self, ws: WebSocket):
        try:
            self._clients.remove(ws)
        except ValueError:
            pass

    def emit(self, event_type: str, payload: dict):
        self._last_event_id += 1
        ev = {
            "id": self._last_event_id,
            "ts": int(time.time() * 1000),
            "type": event_type,
            "payload": payload,
        }
        self._history.append(ev)
        if len(self._history) > self._history_max:
            self._history = self._history[-self._history_max:]
        for ws in list(self._clients):
            try:
                asyncio.create_task(ws.send_json(ev))
            except Exception:
                self.disconnect(ws)


hub = EventHub()
