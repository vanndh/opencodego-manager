"""Login flow — browser automation для получения session.

Следует ТЗ §86: каждый automation action проверяет результат, никаких
«click → success». Реальный флоу (исследовать §20.1–§20.6) подключим
после — пока mock: получает cookies из vault или создаёт фиктивные.
"""


class LoginFlow:
    def __init__(self, browser_pool, session_provider):
        self._pool = browser_pool
        self._session_provider = session_provider

    async def run(self, account) -> dict:
        """Вернуть {'ok': bool, 'auth_method': str, 'cookies_ref': str}."""
        raise NotImplementedError


class MockLoginFlow(LoginFlow):
    """Прототип: без браузера, кладёт mock-cookies в vault."""

    async def run(self, account) -> dict:
        from security import vault
        from auth.totp_manager import TotpManager

        totp = TotpManager(vault.get(f"acc_{account.id}.totp", ""))
        method = "PASSWORD+TOTP" if totp.enabled() else "PASSWORD"

        # реальный login через браузер появится в research-фазе
        # (см. docs/opencode-research.md); mock сохраняет маркер сессии
        ref = f"acc_{account.id}.cookies"
        vault.set(ref, '{"mock_session": true, "ts": "now"}')
        vault.persist()
        return {"ok": True, "auth_method": method, "cookies_ref": ref}
