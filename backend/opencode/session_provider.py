"""SessionProvider — проверка/валидация сессии + HTTP-клиент.

Mock: сессия «валидна», если в vault есть cookies. Реальная проверка
(например GET /me или открытие workspace) — после исследования.
"""


class SessionProvider:
    async def validate(self, account) -> bool:
        raise NotImplementedError


class MockSessionProvider(SessionProvider):
    async def validate(self, account) -> bool:
        from security import vault
        return vault.has(f"acc_{account.id}.cookies")
