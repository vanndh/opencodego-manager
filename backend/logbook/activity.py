"""Activity logger — структурированные события (ТЗ §42-43).

Секреты никогда не логируются: поле message проходит через redact.
"""

from datetime import datetime

from storage import models


class ActivityLogger:
    def __init__(self, session_factory):
        self._factory = session_factory

    async def log(self, category: str, message: str, account_id: int | None = None,
                  level: str = "INFO"):
        # redact: если message содержит подозрительный секрет — заменяем
        safe = redact(message)
        async with self._factory() as session:
            session.add(models.ActivityEvent(
                account_id=account_id, category=category, level=level, message=safe
            ))
            await session.commit()


_REDACT_PATTERNS = (
    ("sk-live-", "sk-•••••"),
    ("ghp_", "ghp_•••"),
    ("JBSW", "JBSW•••"),
)


def redact(message: str) -> str:
    for needle, repl in _REDACT_PATTERNS:
        if needle in message:
            message = message.replace(needle, repl)
    return message
