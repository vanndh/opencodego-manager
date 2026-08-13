"""Стратегии выбора аккаунта.

ТЗ §37–§40. Каждая стратегия — отдельный класс. SMART-скоринг в scoring.py
(не хардкодить в gateway).
"""

from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def select(self, candidates: list, ctx: dict) -> object | None:
        """Вернуть аккаунт или None если нет подходящего."""


class RoundRobin(Strategy):
    def __init__(self):
        self._idx = 0

    def select(self, candidates, ctx):
        if not candidates:
            return None
        acc = candidates[self._idx % len(candidates)]
        self._idx += 1
        return acc


class MostAvailable(Strategy):
    """Максимум доступного usage (5H остаток в первую очередь)."""

    def select(self, candidates, ctx):
        def remaining(a):
            usage = a.usage[-1] if a.usage else None
            if not usage or usage.five_h_total <= 0:
                return 0
            return max(0, usage.five_h_total - usage.five_h_used)
        best = max(candidates, key=remaining, default=None)
        return best


class LeastUsed(Strategy):
    """Минимальный процент usage."""

    def select(self, candidates, ctx):
        def pct(a):
            usage = a.usage[-1] if a.usage else None
            if not usage or usage.five_h_total <= 0:
                return 100
            return usage.five_h_used / usage.five_h_total
        return min(candidates, key=pct, default=None)


class Priority(Strategy):
    """По gateway_priority (меньше = важнее)."""

    def select(self, candidates, ctx):
        return min(candidates, key=lambda a: (a.gateway_priority, a.id), default=None)


class Manual(Strategy):
    """Всегда выбранный вручную аккаунт, пока не сменили."""

    def __init__(self, locked_id: int | None = None):
        self.locked_id = locked_id

    def select(self, candidates, ctx):
        if self.locked_id is None:
            return None
        return next((a for a in candidates if a.id == self.locked_id), None)


class Smart(Strategy):
    """Взвешенный скоринг — см. gateway/scoring.py."""

    def __init__(self, weights: dict | None = None):
        from gateway.scoring import smart_score
        self._smart_score = smart_score
        self._weights = weights

    def select(self, candidates, ctx):
        if not candidates:
            return None
        return max(candidates, key=lambda a: self._smart_score(a, self._weights), default=None)
