"""Маскирование секретов для UI и логов.

Правила:
  password  → ••••••••••
  totp      → JBSW••••••••PX  (первые 4 + последние 2)
  apikey    → sk-••••••••••••••93D (первые 3 + последние 3)
  recovery  → code остаётся UNUSED/USED, значение не показываем
  cookie    → имя + маска значения
"""


def mask_password(value: str | None) -> str:
    return "••••••••••" if value else ""


def mask_middle(value: str | None, keep_front: int, keep_back: int) -> str:
    if not value:
        return ""
    if len(value) <= keep_front + keep_back:
        return "•" * len(value)
    return value[:keep_front] + "•" * 8 + value[-keep_back:]


def mask_totp(value: str | None) -> str:
    return mask_middle(value, 4, 2)


def mask_apikey(value: str | None) -> str:
    return mask_middle(value, 3, 3)


def mask_cookies(value: str | None) -> str:
    """Cookie-хранилище → только «хранится (N байт)» без содержимого."""
    if not value:
        return ""
    return f"<encrypted {len(value)} bytes>"


def mask_credential(kind: str, value: str | None) -> str:
    fn = {
        "password": mask_password,
        "totp": mask_totp,
        "recovery": lambda v: mask_middle(v, 0, 0),
        "apikey": mask_apikey,
        "cookies": mask_cookies,
    }.get(kind, mask_password)
    return fn(value)
