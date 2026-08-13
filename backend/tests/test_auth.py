"""PHASE 5-7 тесты: TOTP, recovery, session, auth orchestrator, worker."""

import asyncio
import tempfile
from pathlib import Path

import pytest

_tmp = Path(tempfile.mkdtemp(prefix="opengom-auth-test-"))


def test_totp_generation_and_verification():
    import pyotp
    from auth.totp_manager import TotpManager

    secret = pyotp.random_base32()
    m = TotpManager(secret)
    code = m.now()
    assert len(code) == 6 and code.isdigit()
    assert m.verify(code)
    assert m.expires_in() <= 30


def test_totp_next_window_when_expiring():
    from auth.totp_manager import TotpManager

    m = TotpManager("JBSWY3DPEHPK3PXP", drift_seconds=25)
    # forced маленький expires_in → next_code ждёт окно и даёт код
    assert len(m.next_code()) == 6


def test_recovery_manager_status_and_use():
    from auth.recovery_manager import RecoveryManager
    from security import vault

    vault._VAULT = {}
    vault._FERNET = None
    rm = RecoveryManager("acc_1.recovery", auto_use=False)
    rm.import_codes("code1\ncode2\ncode3")
    st = rm.status()
    assert st == {"total": 3, "unused": 3, "used": 0}
    nxt = rm.next_unused()
    assert nxt == "code1"
    rm.mark_used("code1")
    assert rm.status()["used"] == 1
    assert rm.next_unused() == "code2"
    assert rm.auto_use is False


@pytest.mark.asyncio
async def test_session_manager_flow():
    import storage.db as dbmod
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

    from auth.session_manager import SessionManager
    from storage.db import init_db
    from storage import repo

    tmp_db = _tmp / "test.db"
    engine = dbmod.make_engine(tmp_db)
    old = dbmod.engine, dbmod.SessionLocal
    dbmod.engine = engine
    dbmod.SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    await init_db()
    async with dbmod.SessionLocal() as s:
        acc = await repo.create_account(s, alias="A", email="s1@gmail.com")
        await s.commit()
        aid = acc.id

    mgr = SessionManager(dbmod.SessionLocal, vault_key="")
    assert await mgr.get(aid) is None
    sess = await mgr.save(aid, cookies_ref="acc_1.cookies", auth_method="PASSWORD+TOTP")
    assert sess.state == "valid"
    assert mgr.is_valid(sess)
    await mgr.mark_expired(aid)
    assert (await mgr.get(aid)).state == "expired"
    await mgr.clear(aid)
    assert await mgr.get(aid) is None

    dbmod.engine, dbmod.SessionLocal = old
    await engine.dispose()


@pytest.mark.asyncio
async def test_worker_refreshes_usage():
    """Mock usage provider + worker: статус online и появляется UsageSnapshot."""
    import storage.db as dbmod
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

    from accounts.worker import AccountWorker
    from core.auth_orchestrator import AuthOrchestrator
    from auth.session_manager import SessionManager
    from automation.login_flow import MockLoginFlow
    from opencode.usage_provider import MockUsageProvider
    from opencode.bonus_provider import MockBonusProvider
    from opencode.session_provider import MockSessionProvider
    from security import vault
    from storage import repo
    from storage.db import init_db

    tmp_db = _tmp / "worker.db"
    engine = dbmod.make_engine(tmp_db)
    old = dbmod.engine, dbmod.SessionLocal
    dbmod.engine = engine
    dbmod.SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    vault._VAULT = {}
    vault._FERNET = None
    await init_db()
    async with dbmod.SessionLocal() as s:
        acc = await repo.create_account(s, alias="W1", email="w1@gmail.com")
        await s.commit()
        aid = acc.id

    auth = AuthOrchestrator(
        SessionManager(dbmod.SessionLocal, ""),
        MockLoginFlow(None, MockSessionProvider()),
        MockSessionProvider(),
    )
    w = AccountWorker(aid, dbmod.SessionLocal, auth, MockUsageProvider(), MockBonusProvider(),
                      poll_interval=0.05)
    w.start()
    await asyncio.sleep(1.0)
    await w.stop()

    async with dbmod.SessionLocal() as s:
        acc = await repo.get_account(s, aid)
        assert acc.status == "online"
        assert len(acc.usage) >= 1
        assert acc.usage[-1].five_h_total == 12.0

    dbmod.engine, dbmod.SessionLocal = old
    await engine.dispose()
