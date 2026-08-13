"""Роутер system — версия/автор/статус БД и vault."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import SystemOut
from config import app as cfg
from security import vault
from storage.db import get_session

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("", response_model=SystemOut)
async def system_info(session: AsyncSession = Depends(get_session)):
    # Проверка БД: выполняем лёгкий SELECT, чтобы вернуть реальный статус.
    db_ok = True
    try:
        from sqlalchemy import text
        await session.execute(text("SELECT 1"))
    except Exception:
        db_ok = False
    return SystemOut(
        name=cfg.APP_NAME,
        slug=cfg.APP_SLUG,
        version=cfg.APP_VERSION,
        author=cfg.APP_AUTHOR,
        db_ready=db_ok,
        vault_locked=not vault.has("_loaded"),
    )
