"""Repository слой — CRUD для доменных сущностей.

Изолирует SQLAlchemy от core/api. PHASE 4: Account, Group, Setting.
"""

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from storage import models

_ACCOUNT_LOAD = (
    selectinload(models.Account.group),
    selectinload(models.Account.sessions),
    selectinload(models.Account.usage),
    selectinload(models.Account.bonuses),
    selectinload(models.Account.api_creds),
)


# ── Account ──────────────────────────────────────────────────────────────────
async def list_accounts(session: AsyncSession) -> list[models.Account]:
    result = await session.execute(
        select(models.Account)
        .options(*_ACCOUNT_LOAD)
        .order_by(models.Account.gateway_priority, models.Account.id)
    )
    return list(result.scalars())


async def get_account(session: AsyncSession, account_id: int) -> models.Account | None:
    result = await session.execute(
        select(models.Account).options(*_ACCOUNT_LOAD).where(models.Account.id == account_id)
    )
    return result.scalar_one_or_none()


async def get_account_by_email(session: AsyncSession, email: str) -> models.Account | None:
    result = await session.execute(
        select(models.Account).where(models.Account.email == email.lower())
    )
    return result.scalar_one_or_none()


async def create_account(
    session: AsyncSession,
    *,
    alias: str,
    email: str,
    group_id: int | None = None,
) -> models.Account:
    acc = models.Account(alias=alias, email=email.lower(), group_id=group_id)
    session.add(acc)
    await session.flush()
    return acc


async def update_account(session: AsyncSession, account: models.Account, **fields) -> models.Account:
    for k, v in fields.items():
        setattr(account, k, v)
    await session.flush()
    return account


async def delete_account(session: AsyncSession, account_id: int) -> bool:
    acc = await session.get(models.Account, account_id)
    if acc is None:
        return False
    await session.delete(acc)
    await session.flush()
    return True


# ── CredentialRef ────────────────────────────────────────────────────────────
async def add_credential_ref(
    session: AsyncSession, *, account_id: int | None, kind: str, vault_key: str
) -> models.CredentialRef:
    ref = models.CredentialRef(account_id=account_id, kind=kind, vault_key=vault_key)
    session.add(ref)
    await session.flush()
    return ref


async def list_credential_refs(session: AsyncSession, account_id: int) -> list[models.CredentialRef]:
    result = await session.execute(
        select(models.CredentialRef).where(models.CredentialRef.account_id == account_id)
    )
    return list(result.scalars())


# ── Group ────────────────────────────────────────────────────────────────────
async def get_or_create_group(session: AsyncSession, name: str) -> models.AccountGroup:
    result = await session.execute(
        select(models.AccountGroup).where(models.AccountGroup.name == name)
    )
    grp = result.scalar_one_or_none()
    if grp is None:
        grp = models.AccountGroup(name=name)
        session.add(grp)
        await session.flush()
    return grp


# ── Setting ──────────────────────────────────────────────────────────────────
async def get_setting(session: AsyncSession, key: str, default: str = "") -> str:
    result = await session.execute(
        select(models.ApplicationSetting).where(models.ApplicationSetting.key == key)
    )
    row = result.scalar_one_or_none()
    return row.value if row is not None else default


async def set_setting(session: AsyncSession, key: str, value: str):
    result = await session.execute(
        select(models.ApplicationSetting).where(models.ApplicationSetting.key == key)
    )
    row = result.scalar_one_or_none()
    if row is None:
        session.add(models.ApplicationSetting(key=key, value=value))
    else:
        row.value = value
    await session.flush()
