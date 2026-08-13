"""BonusProvider — детект и активация бонусов.

Мок-реализация: бонус «появляется» у аккаунтов с бонус-флагом.
Реальный флоу (открыть страницу → scroll → View Reward → Activate → verify)
подключается через automation/bonus_flow после исследования.
"""

from dataclasses import dataclass


@dataclass
class BonusInfo:
    available: bool
    bonus_type: str = "weekly"   # weekly|monthly|one-time
    pct: int = 0


class BonusProvider:
    async def detect(self, account) -> BonusInfo:
        raise NotImplementedError

    async def activate(self, account) -> BonusInfo:
        raise NotImplementedError


class MockBonusProvider(BonusProvider):
    async def detect(self, account) -> BonusInfo:
        # бонус доступен если у аккаунта last_usage.bonus_pct > 0
        if account.usage and account.usage[-1].bonus_pct > 0:
            return BonusInfo(available=True, pct=account.usage[-1].bonus_pct)
        return BonusInfo(available=False)

    async def activate(self, account) -> BonusInfo:
        return BonusInfo(available=True, pct=25)
