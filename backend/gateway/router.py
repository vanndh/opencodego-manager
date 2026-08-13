"""GatewayRouter — выбор аккаунта + failover (ТЗ §35, §41-42).

Не бесконечные retry: один запрос = ≤(retry_count+1) попыток.
"""

import time

from gateway.strategies import (
    LeastUsed, Manual, MostAvailable, Priority, RoundRobin, Smart,
)

STRATEGY_MAP = {
    "round_robin": RoundRobin,
    "most_available": MostAvailable,
    "least_used": LeastUsed,
    "priority": Priority,
    "manual": Manual,
    "smart": Smart,
}


class GatewayRoutingError(Exception):
    pass


class GatewayRouter:
    def __init__(self, strategy_name: str = "most_available",
                 retry_count: int = 1, weights: dict | None = None):
        self.strategy_name = strategy_name
        self.retry_count = retry_count
        self.weights = weights

    def _make_strategy(self):
        cls = STRATEGY_MAP.get(self.strategy_name, MostAvailable)
        if self.strategy_name == "manual":
            return cls()
        if self.strategy_name == "smart":
            return cls(weights=self.weights)
        return cls()

    def route(self, candidates: list, do_call) -> dict:
        """Выполнить do_call(account) с failover.

        do_call должен кидать GatewayRoutingError при сбое аккаунта.
        Возвращает {'account': ..., 'switched': bool, 'result': ...}.
        """
        strategy = self._make_strategy()
        attempts = 0
        used = set()
        switched = False
        while attempts <= self.retry_count:
            attempts += 1
            avail = [a for a in candidates if a.id not in used and not a.paused]
            acc = strategy.select(avail, {})
            if acc is None:
                raise GatewayRoutingError("no available accounts")
            used.add(acc.id)
            try:
                result = do_call(acc)
                return {"account": acc, "switched": switched, "result": result}
            except GatewayRoutingError:
                switched = True
                continue
        raise GatewayRoutingError(f"all {len(used)} accounts failed")
