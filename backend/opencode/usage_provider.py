"""UsageProvider — лимиты 5H / WEEK / MONTH.

Мок-реализация для прототипа. Реальный endpoint после исследования
(см. docs/opencode-research.md §7–§10). Никаких выдуманных схем.
"""

import random
import time
from dataclasses import dataclass


@dataclass
class UsageLimits:
    five_h_used: float
    five_h_total: float
    five_h_reset: str
    weekly_used: float
    weekly_total: float
    weekly_reset: str
    monthly_used: float
    monthly_total: float
    monthly_reset: str
    bonus_pct: int = 0

    def dict(self) -> dict:
        return {
            "five_h": {"used": self.five_h_used, "total": self.five_h_total, "reset": self.five_h_reset},
            "weekly": {"used": self.weekly_used, "total": self.weekly_total, "reset": self.weekly_reset},
            "monthly": {"used": self.monthly_used, "total": self.monthly_total, "reset": self.monthly_reset},
            "bonus_pct": self.bonus_pct,
        }


class UsageProvider:
    """Интерфейс. Реализацию подключить после исследования флоу."""

    async def fetch(self, account) -> UsageLimits:
        raise NotImplementedError


class MockUsageProvider(UsageProvider):
    """Синтетика для прототипа — плавно растёт со временем."""

    async def fetch(self, account) -> UsageLimits:
        # детерминированно от id аккаунта + время — реалистично дрейфует
        seed = account.id * 13 + int(time.time() // 60)
        rnd = random.Random(seed)
        return UsageLimits(
            five_h_used=round(rnd.uniform(2, 12), 1),
            five_h_total=12.0,
            five_h_reset="01:42:17",
            weekly_used=round(rnd.uniform(5, 30), 1),
            weekly_total=30.0,
            weekly_reset="4d 11h",
            monthly_used=round(rnd.uniform(10, 60), 1),
            monthly_total=60.0,
            monthly_reset="18d 02h",
            bonus_pct=rnd.choice([0, 0, 0, 25, 25]),
        )
