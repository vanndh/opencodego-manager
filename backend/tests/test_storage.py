"""PHASE 4 тесты: vault шифрование, маски, БД CRUD, аккаунт creation.

Запуск: cd backend && pytest -q
"""

import asyncio
import tempfile
from pathlib import Path

import pytest

# изолируем данные тестов во временной папке ДО импорта моделей
_tmp = Path(tempfile.mkdtemp(prefix="opengom-test-"))
_tmp_key = _tmp / ".vault-key"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_vault_encrypt_roundtrip():
    from security import vault

    vault._VAULT = {}
    vault._FERNET = None
    vault.set("acc_1.password", "secret123")
    vault.persist()
    assert vault.has("acc_1.password")
    assert vault.get("acc_1.password") == "secret123"


def test_mask_never_leaks():
    from security import mask

    assert mask.mask_password("secret123") == "••••••••••"
    t = mask.mask_totp("JBSWY3DPEHPK3PXP")
    assert "JBSWY3DPEHPK3PXP" not in t
    assert t.startswith("JBSW") and t.endswith("XP")
    k = mask.mask_apikey("sk-live-abc123def456")
    assert k.startswith("sk-") and k.endswith("456")
    assert "abc123def" not in k


@pytest.mark.asyncio
async def test_account_crud():
    from sqlalchemy.ext.asyncio import async_sessionmaker

    from storage import repo
    from storage.db import init_db
    import storage.db as dbmod

    tmp_db = _tmp / "test.db"
    engine = dbmod.make_engine(tmp_db)
    old_engine, old_session = dbmod.engine, dbmod.SessionLocal
    dbmod.engine = engine
    dbmod.SessionLocal = async_sessionmaker(engine, class_=object, expire_on_commit=False)
    # переустановим SessionLocal через фабрику dbmod
    from sqlalchemy.ext.asyncio import AsyncSession
    dbmod.SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    await init_db()
    async with dbmod.SessionLocal() as s:
        acc = await repo.create_account(s, alias="MAIN-01", email="u1@gmail.com")
        assert acc.id is not None
        await s.commit()

        acc2 = await repo.get_account_by_email(s, "U1@GMAIL.COM")
        assert acc2 is not None and acc2.email == "u1@gmail.com"

        ok = await repo.delete_account(s, acc.id)
        assert ok is True
        await s.commit()

    dbmod.engine, dbmod.SessionLocal = old_engine, old_session
    await engine.dispose()
