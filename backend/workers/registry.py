"""WorkerRegistry — управление AccountWorker'ами на всех аккаунтах.

Bounded concurrency через semaphore в BrowserPool. Один worker = аккаунт.
"""

import asyncio

from accounts.worker import AccountWorker


class WorkerRegistry:
    def __init__(self):
        self._workers: dict[int, AccountWorker] = {}
        self._factory = None

    def set_session_factory(self, factory):
        self._factory = factory

    async def sync_accounts(self, account_ids: list[int]):
        """Поднять workers для новых, убить для удалённых."""
        current = set(self._workers)
        wanted = set(account_ids)
        for acc_id in wanted - current:
            worker = AccountWorker(acc_id, self._factory, *self._deps())
            worker.start()
            self._workers[acc_id] = worker
        for acc_id in current - wanted:
            await self._workers[acc_id].stop()
            del self._workers[acc_id]

    def _deps(self):
        """Заглушка — реальные deps собираются в app bootstrap (PHASE 6+)."""
        return (None, None, None)

    async def stop_all(self):
        for w in list(self._workers.values()):
            await w.stop()
        self._workers.clear()
