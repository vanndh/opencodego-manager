"""ApiProvider — импорт существующих API-credentials аккаунта.

Mock: генерирует детерминированный ключ-маску. Реальный endpoint — после
исследования (docs/opencode-research.md §13).
"""


class ApiCredentialInfo:
    def __init__(self, secret: str, label: str = ""):
        self.secret = secret
        self.label = label


class ApiCredentialProvider:
    async def list(self, account) -> list[ApiCredentialInfo]:
        raise NotImplementedError

    async def test(self, secret: str) -> dict:
        raise NotImplementedError


class MockApiCredentialProvider(ApiCredentialProvider):
    async def list(self, account) -> list[ApiCredentialInfo]:
        # детерминированный mock-ключ от id аккаунта (скрытая схема)
        seed = account.id * 17
        fake = f"sk-mock-{seed:08d}-{account.id:04d}MOCK"
        return [ApiCredentialInfo(secret=fake, label="default")]

    async def test(self, secret: str) -> dict:
        return {"ok": True, "latency_ms": 120, "detail": "mock"}
