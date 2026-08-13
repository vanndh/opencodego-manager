"""PHASE 9-10 тесты: gateway strategies, router failover, smart scoring."""

import pytest

from gateway.router import GatewayRouter, GatewayRoutingError
from gateway.scoring import smart_score


class FakeAccount:
    def __init__(self, id, priority=10, paused=False, usage=None, status="online",
                 health="good", latency_ms=0, last_error=None):
        self.id = id
        self.gateway_priority = priority
        self.paused = paused
        self.usage = usage or []
        self.status = status
        self.health = health
        self.latency_ms = latency_ms
        self.last_error = last_error


def _acc_with_usage(id, used, total):
    class U:
        five_h_used = used
        five_h_total = total
    return FakeAccount(id, usage=[U()])


def test_most_available_selects_max_remaining():
    from gateway.strategies import MostAvailable
    a = _acc_with_usage(1, used=10, total=12)   # 2 осталось
    b = _acc_with_usage(2, used=3, total=12)    # 9 осталось
    assert MostAvailable().select([a, b], {}).id == 2


def test_least_used_selects_min_pct():
    from gateway.strategies import LeastUsed
    a = _acc_with_usage(1, used=11, total=12)   # 92%
    b = _acc_with_usage(2, used=2, total=12)    # 17%
    assert LeastUsed().select([a, b], {}).id == 2


def test_priority_respects_gateway_priority():
    from gateway.strategies import Priority
    a = FakeAccount(1, priority=3)
    b = FakeAccount(2, priority=1)
    assert Priority().select([a, b], {}).id == 2


def test_round_robin_cycles():
    from gateway.strategies import RoundRobin
    rr = RoundRobin()
    a, b = FakeAccount(1), FakeAccount(2)
    assert rr.select([a, b], {}).id == 1
    assert rr.select([a, b], {}).id == 2
    assert rr.select([a, b], {}).id == 1


def test_manual_locks_account():
    from gateway.strategies import Manual
    a, b = FakeAccount(1), FakeAccount(2)
    assert Manual(locked_id=2).select([a, b], {}).id == 2
    assert Manual(locked_id=99).select([a, b], {}) is None


def test_router_failover_switches_account():
    calls = []

    def do_call(acc):
        calls.append(acc.id)
        raise GatewayRoutingError("boom")

    router = GatewayRouter(strategy_name="round_robin", retry_count=2)
    with pytest.raises(GatewayRoutingError):
        router.route([FakeAccount(1), FakeAccount(2)], do_call)
    # оба аккаунта использованы, третий retry — кандидатов нет
    assert len(calls) == 2


def test_router_returns_result_on_success():
    def do_call(acc):
        return {"echo": acc.id}

    router = GatewayRouter(strategy_name="priority", retry_count=1)
    out = router.route([FakeAccount(1, priority=2), FakeAccount(2, priority=1)], do_call)
    assert out["result"] == {"echo": 2}


def test_router_skips_paused():
    def do_call(acc):
        return {"echo": acc.id}
    router = GatewayRouter(strategy_name="most_available", retry_count=0)
    paused = _acc_with_usage(1, used=1, total=12)
    paused.paused = True
    free = _acc_with_usage(2, used=11, total=12)
    out = router.route([paused, free], do_call)
    assert out["account"].id == 2


def test_smart_score_prefers_healthy_available():
    good = _acc_with_usage(1, used=2, total=12)
    bad = _acc_with_usage(2, used=2, total=12)
    bad.status = "error"
    bad.health = "error"
    assert smart_score(good) > smart_score(bad)
