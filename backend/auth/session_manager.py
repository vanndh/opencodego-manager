"""Session-менеджер: cookies, state, expiration, validation, relogin.

Основное правило: не делать полный login каждый раз. Сохранённая сессия
валидируется; при invalid — reauthenticate.
"""

from datetime import datetime

from storage import models


class SessionManager:
    """Работает через session_factory — каждая операция открывает свою сессию.

    Так worker'ы (у которых своя сессия на тик) не конфликтуют с session-записями.
    """

    def __init__(self, session_factory, vault_key: str = ""):
        self._factory = session_factory
        self.vault_key = vault_key

    # ── состояние ────────────────────────────────────────────────────────────
    async def get(self, account_id: int) -> models.Session | None:
        async with self._factory() as session:
            rows = await _list_sessions(session, account_id)
        if not rows:
            return None
        return max(rows, key=lambda s: s.created_at or datetime.min)

    def is_valid(self, sess: models.Session | None) -> bool:
        return sess is not None and sess.state == "valid"

    # ── сохранение ───────────────────────────────────────────────────────────
    async def save(self, account_id: int, cookies_ref: str, auth_method: str) -> models.Session:
        async with self._factory() as session:
            sess = models.Session(
                account_id=account_id,
                vault_key=cookies_ref,
                state="valid",
                auth_method=auth_method,
                last_check=datetime.utcnow(),
            )
            session.add(sess)
            await session.commit()
            return sess

    async def mark_expired(self, account_id: int):
        async with self._factory() as session:
            rows = await _list_sessions(session, account_id)
            for s in rows:
                s.state = "expired"
            await session.commit()

    async def mark_checked(self, account_id: int, valid: bool):
        async with self._factory() as session:
            rows = await _list_sessions(session, account_id)
            for s in rows:
                s.last_check = datetime.utcnow()
                if not valid:
                    s.state = "expired"
            await session.commit()

    async def clear(self, account_id: int):
        async with self._factory() as session:
            rows = await _list_sessions(session, account_id)
            for s in rows:
                await session.delete(s)
            await session.commit()


async def _list_sessions(session, account_id: int) -> list[models.Session]:
    from sqlalchemy import select
    result = await session.execute(
        select(models.Session).where(models.Session.account_id == account_id)
    )
    return list(result.scalars())
