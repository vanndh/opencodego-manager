"""Роутер accounts — CRUD + запись credentials в vault.

Секреты: принимаем на запись (→ vault), наружу отдаём только маски.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api import schemas
from security import mask, vault
from storage import repo
from storage.db import get_session

router = APIRouter(prefix="/api/accounts", tags=["accounts"])


def _to_out(acc, session_state: str = "") -> schemas.AccountOut:
    """Собрать маскированный AccountOut из модели."""
    usage = None
    if acc.usage:
        last = acc.usage[-1]
        usage = schemas.UsageOut(
            five_h_used=last.five_h_used,
            five_h_total=last.five_h_total,
            five_h_reset=last.five_h_reset,
            weekly_used=last.weekly_used,
            weekly_total=last.weekly_total,
            weekly_reset=last.weekly_reset,
            monthly_used=last.monthly_used,
            monthly_total=last.monthly_total,
            monthly_reset=last.monthly_reset,
            bonus_pct=last.bonus_pct,
        )
    totp_raw = vault.get(f"acc_{acc.id}.totp", "")
    return schemas.AccountOut(
        id=acc.id,
        alias=acc.alias,
        email=acc.email,
        group=acc.group.name if acc.group else None,
        status=acc.status,
        health=acc.health,
        auto_relogin=acc.auto_relogin,
        auto_activate_bonus=acc.auto_activate_bonus,
        use_in_gateway=acc.use_in_gateway,
        gateway_priority=acc.gateway_priority,
        paused=acc.paused,
        favorite=acc.favorite,
        last_login=acc.last_login,
        last_update=acc.last_update,
        last_error=acc.last_error,
        latency_ms=acc.latency_ms,
        usage=usage,
        totp_masked=mask.mask_totp(totp_raw),
        recovery_used=0,
        session_state=session_state,
    )


@router.get("", response_model=list[schemas.AccountOut])
async def list_accounts(session: AsyncSession = Depends(get_session)):
    accounts = await repo.list_accounts(session)
    return [_to_out(a) for a in accounts]


@router.post("", response_model=schemas.AccountOut, status_code=201)
async def create_account(
    body: schemas.AccountCreate,
    session: AsyncSession = Depends(get_session),
):
    existing = await repo.get_account_by_email(session, body.email)
    if existing is not None:
        raise HTTPException(409, "account already exists")

    group_id = None
    if body.group:
        grp = await repo.get_or_create_group(session, body.group)
        group_id = grp.id

    acc = await repo.create_account(
        session,
        alias=body.alias or body.email.split("@")[0][:20],
        email=body.email,
        group_id=group_id,
    )
    # секреты → vault (refs в БД)
    if body.password:
        vault.set(f"acc_{acc.id}.password", body.password)
        await repo.add_credential_ref(session, account_id=acc.id, kind="password", vault_key=f"acc_{acc.id}.password")
    if body.totp_secret:
        vault.set(f"acc_{acc.id}.totp", body.totp_secret)
        await repo.add_credential_ref(session, account_id=acc.id, kind="totp", vault_key=f"acc_{acc.id}.totp")
    if body.recovery_codes:
        clean = [c.strip() for c in body.recovery_codes if c.strip()]
        if clean:
            vault.set(f"acc_{acc.id}.recovery", "\n".join(clean))
            await repo.add_credential_ref(session, account_id=acc.id, kind="recovery", vault_key=f"acc_{acc.id}.recovery")

    await session.commit()
    vault.persist()
    return _to_out(acc)


@router.get("/{account_id}", response_model=schemas.AccountOut)
async def get_account(account_id: int, session: AsyncSession = Depends(get_session)):
    acc = await repo.get_account(session, account_id)
    if acc is None:
        raise HTTPException(404, "account not found")
    return _to_out(acc)


@router.patch("/{account_id}", response_model=schemas.AccountOut)
async def update_account(
    account_id: int,
    body: schemas.AccountUpdate,
    session: AsyncSession = Depends(get_session),
):
    acc = await repo.get_account(session, account_id)
    if acc is None:
        raise HTTPException(404, "account not found")
    fields = body.model_dump(exclude_unset=True, exclude={"group"})
    if body.group is not None:
        grp = await repo.get_or_create_group(session, body.group)
        fields["group_id"] = grp.id
    await repo.update_account(session, acc, **fields)
    await session.commit()
    return _to_out(acc)


@router.delete("/{account_id}", status_code=204)
async def delete_account(account_id: int, session: AsyncSession = Depends(get_session)):
    ok = await repo.delete_account(session, account_id)
    if not ok:
        raise HTTPException(404, "account not found")
    for kind in ("password", "totp", "recovery", "cookies"):
        vault.delete(f"acc_{account_id}.{kind}")
    await session.commit()
    vault.persist()
