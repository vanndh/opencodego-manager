"""Роутер API credentials — импорт существующих ключей аккаунта (ТЗ §31-33).

Mock-провайдер: детерминированные ключи. Реальный импорт — после
исследования (docs/opencode-research.md §13). Наружу — только маски.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from opencode.api_provider import MockApiCredentialProvider
from security import mask, vault
from storage import models, repo
from storage.db import get_session

router = APIRouter(prefix="/api/creds", tags=["api-creds"])
_provider = MockApiCredentialProvider()


@router.get("/{account_id}")
async def list_creds(account_id: int, session: AsyncSession = Depends(get_session)):
    acc = await repo.get_account(session, account_id)
    if acc is None:
        raise HTTPException(404, "account not found")
    # import существующих ключей из провайдера (или берём сохранённые)
    stored = [c for c in acc.api_creds if c.status == "active"]
    if not stored:
        for info in await _provider.list(acc):
            ref = f"acc_{account_id}.apikey_{len(acc.api_creds)+1}"
            vault.set(ref, info.secret)
            session.add(models.ApiCredential(
                account_id=account_id, secret_ref=ref, label=info.label, status="active"
            ))
        await session.commit()
        acc = await repo.get_account(session, account_id)
        stored = [c for c in acc.api_creds if c.status == "active"]
    return [
        {"id": c.id, "label": c.label, "status": c.status,
         "masked": mask.mask_apikey(vault.get(c.secret_ref, "")),
         "latency_ms": c.latency_ms, "last_test": c.last_test}
        for c in stored
    ]


@router.post("/{cred_id}/test")
async def test_cred(cred_id: int, session: AsyncSession = Depends(get_session)):
    cred = await session.get(models.ApiCredential, cred_id)
    if cred is None:
        raise HTTPException(404, "credential not found")
    res = await _provider.test(vault.get(cred.secret_ref, ""))
    cred.last_test = models.datetime.utcnow()
    cred.latency_ms = res.get("latency_ms", 0)
    await session.commit()
    return res


@router.post("/{cred_id}/disable")
async def disable_cred(cred_id: int, session: AsyncSession = Depends(get_session)):
    cred = await session.get(models.ApiCredential, cred_id)
    if cred is None:
        raise HTTPException(404, "credential not found")
    cred.status = "disabled"  # локально, remote не трогаем
    await session.commit()
    return {"ok": True}
