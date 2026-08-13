"""AuthOrchestrator — связывает login_manager / totp / session.

Алгоритм (ТЗ §15):
  session valid → reuse
  иначе → login: email → password → 2FA → TOTP → submit → save session
"""

from auth.session_manager import SessionManager
from auth.totp_manager import TotpManager
from automation.login_flow import LoginFlow
from opencode.session_provider import SessionProvider


class AuthOrchestrator:
    def __init__(self, sessions: SessionManager, login_flow: LoginFlow,
                 session_provider: SessionProvider):
        self._sessions = sessions
        self._login_flow = login_flow
        self._session_provider = session_provider

    async def ensure_session(self, account) -> bool:
        """Валидна сессия? reuse. Иначе — login через flow."""
        sess = await self._sessions.get(account.id)
        if sess is not None and self._sessions.is_valid(sess):
            if await self._session_provider.validate(account):
                await self._sessions.mark_checked(account.id, True)
                return True
            await self._sessions.mark_checked(account.id, False)

        # reauthenticate
        res = await self._login_flow.run(account)
        if res.get("ok"):
            await self._sessions.save(
                account.id,
                cookies_ref=res.get("cookies_ref", ""),
                auth_method=res.get("auth_method", ""),
            )
            return True
        return False
