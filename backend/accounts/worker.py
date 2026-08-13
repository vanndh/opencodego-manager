"""AccountWorker — независимый async-цикл на аккаунт.

- SessionManager (valid → use / relogin)
- UsageWorker: периодический fetch лимитов (+jitter)
- BonusWorker: детект → auto-activate → verify
- HealthMonitor: GOOD/DEGRADED/ERROR/OFFLINE
Ошибка одного аккаунта не блокирует остальных.
"""

import asyncio
import random
import time

from core.auth_orchestrator import AuthOrchestrator
from opencode.usage_provider import UsageProvider
from opencode.bonus_provider import BonusProvider
from storage import models, repo


class AccountWorker:
    def __init__(self, account_id: int, session_factory,
                 auth: AuthOrchestrator, usage: UsageProvider,
                 bonus: BonusProvider, poll_interval: float = 60.0):
        self.account_id = account_id
        self._session_factory = session_factory
        self._auth = auth
        self._usage = usage
        self._bonus = bonus
        self._poll_interval = poll_interval
        self._stop = asyncio.Event()
        self._task: asyncio.Task | None = None
        self.status = "idle"
        self.last_error = ""
        self.last_latency_ms = 0

    def start(self):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._loop())

    async def stop(self):
        self._stop.set()
        if self._task:
            await self._task

    async def _loop(self):
        while not self._stop.is_set():
            try:
                await self._tick()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.status = "error"
                self.last_error = str(e)[:200]
            await self._wait_poll()

    async def _wait_poll(self):
        # с jitter — разнесём запросы
        jitter = random.uniform(0, 5)
        try:
            await asyncio.wait_for(self._stop.wait(), timeout=self._poll_interval + jitter)
        except asyncio.TimeoutError:
            pass

    async def _tick(self):
        async with self._session_factory() as session:
            account = await repo.get_account(session, self.account_id)
            if account is None:
                self.status = "error"
                return

            # 1. сессия
            if not await self._auth.ensure_session(account):
                self.status = "error"
                self.last_error = "session invalid"
                account.status = "error"
                await session.commit()
                return

            # 2. usage
            t0 = time.time()
            limits = await self._usage.fetch(account)
            self.last_latency_ms = int((time.time() - t0) * 1000)
            account.usage.append(models.UsageSnapshot(
                account_id=account.id,
                five_h_used=limits.five_h_used, five_h_total=limits.five_h_total,
                five_h_reset=limits.five_h_reset,
                weekly_used=limits.weekly_used, weekly_total=limits.weekly_total,
                weekly_reset=limits.weekly_reset,
                monthly_used=limits.monthly_used, monthly_total=limits.monthly_total,
                monthly_reset=limits.monthly_reset,
                bonus_pct=limits.bonus_pct,
            ))
            account.last_update = models.datetime.utcnow()
            account.latency_ms = self.last_latency_ms
            account.status = "online"
            self.status = "online"

            # 3. бонусы (detect + auto)
            bonus = await self._bonus.detect(account)
            if bonus.available:
                account.status = "online"  # бонус не меняет статус
                if account.auto_activate_bonus:
                    await self._bonus.activate(account)

            await session.commit()
            self.last_error = ""
