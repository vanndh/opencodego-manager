"""Vault — шифрованное хранилище секретов (Fernet / AES-128-CBC + HMAC).

Все пароли, TOTP-секреты, recovery-коды, cookies, API-ключи живут здесь.
DB хранит только CredentialRef → vault_key.
Master key: OS keyring (default) или файл-ключ (fallback).
"""

import base64
import json
import threading

from cryptography.fernet import Fernet

from security import keyring_adapter

_LOCK = threading.Lock()
_VAULT: dict[str, str] = {}
_FERNET: Fernet | None = None


def _get_fernet() -> Fernet:
    global _FERNET
    if _FERNET is None:
        key, used = keyring_adapter.get_master_key()
        if not used:
            # стараемся переселить в keyring для будущих запусков
            keyring_adapter.store_master_key(key)
        _FERNET = Fernet(base64.urlsafe_b64encode(key).decode("ascii"))
    return _FERNET


def unlock():
    """Загрузить vault.bin в RAM (мастер-ключ из keyring/файла)."""
    global _VAULT
    with _LOCK:
        fernet = _get_fernet()
        from config.app import VAULT_PATH
        if VAULT_PATH.exists():
            try:
                blob = VAULT_PATH.read_bytes()
                data = json.loads(fernet.decrypt(blob).decode("utf-8"))
                _VAULT = data if isinstance(data, dict) else {}
            except Exception:
                _VAULT = {}
        else:
            _VAULT = {}
        _VAULT["_loaded"] = "1"


def lock():
    """Выгрузить vault из RAM (секреты не держим без необходимости)."""
    global _VAULT
    with _LOCK:
        _VAULT = {}


def get(key: str, default=None):
    with _LOCK:
        return _VAULT.get(key, default)


def set(key: str, value: str):
    with _LOCK:
        _VAULT[key] = value


def delete(key: str):
    with _LOCK:
        _VAULT.pop(key, None)


def persist():
    """Переписать vault.bin шифрованным blob текущего состояния."""
    with _LOCK:
        fernet = _get_fernet()
        from config.app import VAULT_PATH
        blob = fernet.encrypt(json.dumps(_VAULT, ensure_ascii=False).encode("utf-8"))
        tmp = VAULT_PATH.with_suffix(".tmp")
        tmp.write_bytes(blob)
        tmp.replace(VAULT_PATH)


def has(key: str) -> bool:
    with _LOCK:
        return key in _VAULT
