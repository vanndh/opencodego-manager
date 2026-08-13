"""Роутер bonuses — детект/активация бонусов + история (ТЗ §27-30).

Mock-реализация (см. opencode/bonus_provider). Реальный флоу активации —
после исследования.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from opencode.bonus_provider import MockBonusProvider
from storage import repo
from storage.db import get_session

router = APIRouter(prefix="/api/bonuses", tags=["bonuses"])
_provider = MockBonusProvider()


@router.get("")
async def list_bonuses(session: AsyncSession = Depends(get_session)):
    accounts = await repo.list_accounts(session)
    out = []
    for acc in accounts:
        info = await _provider.detect(acc)
        if info.available:
            out.append({"account_id": acc.id, "alias": acc.alias, "type": info.bonus_type, "pct": info.pct})
    return out


@router.post("/{account_id}/activate")
async def activate_bonus(account_id: int, session: AsyncSession = Depends(get_session)):
    acc = await repo.get_account(session, account_id)
    if acc is None:
        raise HTTPException(404, "account not found")
    info = await _provider.activate(acc)
    return {"account_id": account_id, "ok": True, "type": info.bonus_type, "pct": info.pct}
