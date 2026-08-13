from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ── Входящие ─────────────────────────────────────────────────────────────────
class AccountCreate(BaseModel):
    alias: str = ""
    email: EmailStr
    password: str | None = None
    totp_secret: str | None = None
    recovery_codes: list[str] = Field(default_factory=list)
    group: str | None = None


class AccountUpdate(BaseModel):
    alias: str | None = None
    group: str | None = None
    auto_relogin: bool | None = None
    auto_activate_bonus: bool | None = None
    use_in_gateway: bool | None = None
    gateway_priority: int | None = None
    paused: bool | None = None
    favorite: bool | None = None


class CredentialSet(BaseModel):
    kind: str  # password|totp|recovery|cookies|apikey
    value: str


# ── Исходящие (маскированные) ───────────────────────────────────────────────
class UsageOut(BaseModel):
    five_h_used: float = 0
    five_h_total: float = 0
    five_h_reset: str | None = None
    weekly_used: float = 0
    weekly_total: float = 0
    weekly_reset: str | None = None
    monthly_used: float = 0
    monthly_total: float = 0
    monthly_reset: str | None = None
    bonus_pct: int = 0


class AccountOut(BaseModel):
    id: int
    alias: str
    email: str
    group: str | None = None
    status: str
    health: str
    auto_relogin: bool
    auto_activate_bonus: bool
    use_in_gateway: bool
    gateway_priority: int
    paused: bool
    favorite: bool
    last_login: datetime | None = None
    last_update: datetime | None = None
    last_error: str | None = None
    latency_ms: int = 0
    usage: UsageOut | None = None
    password_masked: str = "••••••••••"
    totp_masked: str = ""
    recovery_used: int = 0
    session_state: str = ""


class SystemOut(BaseModel):
    name: str
    slug: str
    version: str
    author: str
    db_ready: bool
    vault_locked: bool
