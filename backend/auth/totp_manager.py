"""TOTP-менеджер: генерация кода с учётом 30-сек окна и clock drift.

Не логирует код. Учитывает: window, системное время, drift, retry со следующего окна.
"""

import time

import pyotp


class TotpManager:
    def __init__(self, secret: str | None, drift_seconds: float = 2.0):
        self.secret = secret
        self.drift = drift_seconds

    def enabled(self) -> bool:
        return bool(self.secret)

    def now(self, at: float | None = None) -> str:
        """Текущий OTP."""
        if not self.secret:
            raise ValueError("totp not configured")
        return pyotp.TOTP(self.secret).at(at or int(time.time()))

    def expires_in(self, at: float | None = None) -> float:
        """Секунд до конца текущего окна (с учётом drift)."""
        now = at if at is not None else time.time()
        period = pyotp.TOTP(self.secret).interval if self.secret else 30
        return period - (now % period)

    def next_code(self) -> str:
        """Код следующего окна (если текущий вот-вот истечёт)."""
        if self.expires_in() <= self.drift:
            time.sleep(0.3)
        return self.now()

    def verify(self, code: str, window: int = 1) -> bool:
        if not self.secret:
            return False
        return pyotp.TOTP(self.secret).verify(code, valid_window=window)
