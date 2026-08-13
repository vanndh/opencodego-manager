"""Модели данных (SQLAlchemy 2.0, async).

Схема соответствует ARCHITECTURE.md §7. Account ↔ CredentialRef — indirection:
DB хранит только ссылку на vault (ключ), секреты живут в vault.bin.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.db import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    alias: Mapped[str] = mapped_column(String(64), default="")
    email: Mapped[str] = mapped_column(String(255), index=True)
    group_id: Mapped[int | None] = mapped_column(ForeignKey("account_groups.id"), nullable=True)

    status: Mapped[str] = mapped_column(String(32), default="offline")
    # health: good | degraded | error | offline
    health: Mapped[str] = mapped_column(String(16), default="offline")

    auto_relogin: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_activate_bonus: Mapped[bool] = mapped_column(Boolean, default=False)
    use_in_gateway: Mapped[bool] = mapped_column(Boolean, default=True)
    gateway_priority: Mapped[int] = mapped_column(Integer, default=10)
    paused: Mapped[bool] = mapped_column(Boolean, default=False)
    favorite: Mapped[bool] = mapped_column(Boolean, default=False)

    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_update: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    sessions: Mapped[list["Session"]] = relationship(back_populates="account", cascade="all, delete-orphan")
    usage: Mapped[list["UsageSnapshot"]] = relationship(back_populates="account", cascade="all, delete-orphan")
    bonuses: Mapped[list["Bonus"]] = relationship(back_populates="account", cascade="all, delete-orphan")
    api_creds: Mapped[list["ApiCredential"]] = relationship(back_populates="account", cascade="all, delete-orphan")
    group: Mapped["AccountGroup | None"] = relationship(back_populates="accounts")


class CredentialRef(Base):
    """Ссылка на секрет в vault. kind: password|totp|recovery|cookies|apikey."""

    __tablename__ = "credential_refs"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"), nullable=True, index=True)
    kind: Mapped[str] = mapped_column(String(32))  # password|totp|recovery|cookies|apikey
    vault_key: Mapped[str] = mapped_column(String(128))  # ключ в vault.bin (например "acc_42.totp")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    # cookies хранятся в vault под vault_key; в БД — только ref
    vault_key: Mapped[str] = mapped_column(String(128), default="")
    state: Mapped[str] = mapped_column(String(32), default="valid")  # valid|expired|unknown
    auth_method: Mapped[str] = mapped_column(String(32), default="")  # PASSWORD|PASSWORD+TOTP|RECOVERY
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_check: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    expires_at_est: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    account: Mapped["Account"] = relationship(back_populates="sessions")


class UsageSnapshot(Base):
    __tablename__ = "usage_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    five_h_used: Mapped[float] = mapped_column(default=0)
    five_h_total: Mapped[float] = mapped_column(default=0)
    five_h_reset: Mapped[str | None] = mapped_column(String(64), nullable=True)
    weekly_used: Mapped[float] = mapped_column(default=0)
    weekly_total: Mapped[float] = mapped_column(default=0)
    weekly_reset: Mapped[str | None] = mapped_column(String(64), nullable=True)
    monthly_used: Mapped[float] = mapped_column(default=0)
    monthly_total: Mapped[float] = mapped_column(default=0)
    monthly_reset: Mapped[str | None] = mapped_column(String(64), nullable=True)
    bonus_pct: Mapped[int] = mapped_column(Integer, default=0)
    captured_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    account: Mapped["Account"] = relationship(back_populates="usage")


class Bonus(Base):
    __tablename__ = "bonuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    type: Mapped[str] = mapped_column(String(32), default="weekly")  # weekly|monthly|one-time
    available: Mapped[bool] = mapped_column(Boolean, default=False)
    eligible: Mapped[bool] = mapped_column(Boolean, default=False)
    last_checked: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    account: Mapped["Account"] = relationship(back_populates="bonuses")


class BonusEvent(Base):
    __tablename__ = "bonus_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    type: Mapped[str] = mapped_column(String(32), default="")
    detected_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    result: Mapped[str] = mapped_column(String(32), default="pending")  # pending|ok|failed
    limit_before: Mapped[str | None] = mapped_column(Text, nullable=True)
    limit_after: Mapped[str | None] = mapped_column(Text, nullable=True)


class ApiCredential(Base):
    __tablename__ = "api_credentials"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    secret_ref: Mapped[str] = mapped_column(String(128), default="")  # vault key
    label: Mapped[str] = mapped_column(String(64), default="")
    status: Mapped[str] = mapped_column(String(16), default="active")  # active|disabled
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_used: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_test: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    account: Mapped["Account"] = relationship(back_populates="api_creds")


class GatewayConfig(Base):
    __tablename__ = "gateway_config"

    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    host: Mapped[str] = mapped_column(String(64), default="127.0.0.1")
    port: Mapped[int] = mapped_column(Integer, default=3456)
    access_key_ref: Mapped[str] = mapped_column(String(128), default="")
    strategy: Mapped[str] = mapped_column(String(32), default="most_available")
    group_id: Mapped[int | None] = mapped_column(ForeignKey("account_groups.id"), nullable=True)
    request_timeout_s: Mapped[int] = mapped_column(Integer, default=30)
    retry_count: Mapped[int] = mapped_column(Integer, default=1)
    max_concurrent: Mapped[int] = mapped_column(Integer, default=5)
    autostart: Mapped[bool] = mapped_column(Boolean, default=False)


class GatewayRequest(Base):
    __tablename__ = "gateway_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    ts: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    account_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="ok")  # ok|failed|switched
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class AccountGroup(Base):
    __tablename__ = "account_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    accounts: Mapped[list["Account"]] = relationship(back_populates="group")


class ActivityEvent(Base):
    __tablename__ = "activity_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    ts: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    account_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"), nullable=True)
    category: Mapped[str] = mapped_column(String(16), default="INFO")  # AUTH|LIMITS|BONUSES|GATEWAY|ERRORS
    level: Mapped[str] = mapped_column(String(8), default="INFO")  # DEBUG|INFO|WARNING|ERROR
    message: Mapped[str] = mapped_column(Text, default="")


class ApplicationSetting(Base):
    __tablename__ = "application_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    value: Mapped[str] = mapped_column(Text, default="")
