# Architecture — OpenCode GO Manager

## Stack
- Frontend: React + TypeScript + Vite + Tailwind
- Backend: Python 3.12 + FastAPI + uvicorn
- Browser automation: Playwright (patchright)
- Storage: SQLite (WAL mode, SQLAlchemy 2.0 async)
- Secure vault: cryptography.Fernet (AES-128) + OS keyring optional
- Realtime: WebSocket (fastapi)
- Process: single process, FastAPI serves frontend dist/

## Layers
```
api/          → FastAPI routers (thin HTTP/WS)
core/         → domain services (no HTTP, no Playwright)
opencode/     → integration providers (interface + impl + mock)
automation/   → browser layer (Playwright only here)
gateway/      → local API proxy server (separate port)
storage/      → SQLite + vault
security/     → encryption, masking, keyring
workers/      → scheduler, semaphore, periodic loops
accounts/     → AccountWorker, SessionManager, HealthMonitor
auth/         → login_manager, totp, recovery, session
notifications/→ local toast + system notify
logging/      → structlog, redaction filters
config/       → app settings, runtime config
```

## Data Models (SQLite)
- Account, CredentialRef, Session, UsageSnapshot
- Bonus, BonusEvent, ApiCredential
- GatewayCfg, GatewayRequest, ActivityEvent
- AccountGroup, ApplicationSetting

## Secrets
- DB stores CredentialRef (kind + vault key)
- Vault stores encrypted values (password, totp, recovery, cookies, apikeys)
- Master key: OS keyring (default) or user passphrase (PBKDF2)
- All UI display: masked (sk-••••••93D, ••••••••, JBSW••••••PX)
- All logs: secrets redacted via structlog processor

## Workers
- Each account = AccountWorker (async task)
- Bounded Semaphore(N) for remote concurrency
- Browser pool semaphore (MAX_BROWSERS=3) — only on login
- Session valid → HTTP client (no browser)
- Session expired → relogin via automation
- Exponential backoff 2→5→15s + jitter on errors

## Gateway
- Separate port (127.0.0.1:3456)
- Local Access Key auth (vault)
- Strategies: round_robin, most_available, least_used, priority, manual, smart
- Failover: retry_count then switch account
- Stats: requests, success, errors, avg latency, switches, uptime

## Realtime
- WS hub: in-process event bus → single connection per tab
- Events: account.updated, bonus.detected, gateway.switched, session.expired
- Resume via last_event_id
- Per-account debounce (≤1 event/s)

## Research Required (docs/opencode-research.md)
1. Login flow (sso/github/google)
2. Password auth structure
3. 2FA/TOTP flow
4. Session/cookie behavior
5. Session expiration
6. Workspace flow
7. 5H limit source
8. Weekly limit source
9. Monthly limit source
10. Reset timestamps format
11. Bonus availability
12. Bonus activation flow
13. API credentials page
14. Headers needed
15. Error formats
16. Rate limits
17. Logout/expired signals
18. Bonus reset semantics
> Until confirmed: providers stay Mock (no fake endpoints)