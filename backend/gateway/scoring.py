"""SMART-скоринг аккаунтов (ТЗ §38). Отдельный модуль, не в gateway.

score = w_avail * availability + w_health * health_norm
      + w_reset * reset_proximity + w_success * success_rate
      - w_latency * latency_norm - w_error * recent_errors
"""

DEFAULT_WEIGHTS = {
    "availability": 0.30,
    "health": 0.25,
    "reset": 0.15,
    "success": 0.15,
    "latency": 0.10,
    "error": 0.05,
}

HEALTH_NORM = {"good": 1.0, "degraded": 0.5, "error": 0.0, "offline": 0.0}


def smart_score(account, weights: dict | None = None) -> float:
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    usage = account.usage[-1] if account.usage else None

    # availability: 0..1 (5H остаток)
    if usage and usage.five_h_total > 0:
        avail = max(0.0, min(1.0, (usage.five_h_total - usage.five_h_used) / usage.five_h_total))
    else:
        avail = 0.5

    health = HEALTH_NORM.get(account.health, 0.5)
    reset_prox = 0.5  # фикс для mock; реально — ближе к reset, тем лучше
    success_rate = 0.9 if account.status == "online" else 0.5
    latency = min(1.0, (account.latency_ms or 0) / 2000.0)
    errors = 0.1 if account.last_error else 0.0

    return (
        w["availability"] * avail
        + w["health"] * health
        + w["reset"] * reset_prox
        + w["success"] * success_rate
        - w["latency"] * latency
        - w["error"] * errors
    )
