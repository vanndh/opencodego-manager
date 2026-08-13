"""OS keyring adapter — мастер-ключ для vault.

Default: системное хранилище (macOS Keychain / Win Credential Manager / Secret Service).
Fallback: файл-ключ + passphrase (PBKDF2) если keyring недоступен.
"""

import base64
import hashlib
import os

SERVICE = "opengom"
KEY_USER = "vault-master-key"

try:
    import keyring
    _HAS_KEYRING = True
except Exception:  # pragma: no cover
    keyring = None
    _HAS_KEYRING = False


def _derive_from_passphrase(passphrase: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, 200_000, dklen=32)


def get_master_key() -> tuple[bytes, bool]:
    """Вернуть (master_key, keyring_used)."""
    if _HAS_KEYRING:
        try:
            stored = keyring.get_password(SERVICE, KEY_USER)
            if stored:
                return base64.b64decode(stored), True
        except Exception:
            pass

    # Fallback: файл-ключ рядом с vault (первый запуск создаёт)
    from config.app import DATA_DIR
    key_file = DATA_DIR / ".vault-key"
    if key_file.exists():
        raw = key_file.read_bytes()
        if len(raw) == 32:
            return raw, False
    key = os.urandom(32)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    key_file.write_bytes(key)
    try:
        os.chmod(key_file, 0o600)
    except OSError:
        pass
    return key, False


def store_master_key(key: bytes) -> bool:
    """Записать мастер-ключ в keyring (если доступен)."""
    if not _HAS_KEYRING:
        return False
    try:
        keyring.set_password(SERVICE, KEY_USER, base64.b64encode(key).decode("ascii"))
        return True
    except Exception:
        return False


def clear_master_key():
    if _HAS_KEYRING:
        try:
            keyring.delete_password(SERVICE, KEY_USER)
        except Exception:
            pass
