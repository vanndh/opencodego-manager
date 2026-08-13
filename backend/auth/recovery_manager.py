"""Recovery-менеджер: хранение кодов, статусы UNUSED/USED/UNKNOWN.

Коды живут в vault (зашифрованы), в БД — только ref. Использование recovery
включается опцией AUTO_USE_RECOVERY (default OFF).
"""

import json


class RecoveryManager:
    def __init__(self, vault_key: str, auto_use: bool = False):
        self.vault_key = vault_key
        self.auto_use = auto_use

    def _load(self) -> list[dict]:
        from security import vault
        raw = vault.get(self.vault_key, "")
        if not raw:
            return []
        try:
            data = json.loads(raw)
            return data if isinstance(data, list) else []
        except Exception:
            # устаревший формат — plain list строк
            return [{"code": c, "used": False} for c in raw.splitlines() if c.strip()]

    def _save(self, codes: list[dict]):
        from security import vault
        vault.set(self.vault_key, json.dumps(codes, ensure_ascii=False))
        vault.persist()

    def count(self) -> int:
        return len(self._load())

    def status(self) -> dict:
        codes = self._load()
        unused = sum(1 for c in codes if not c["used"])
        used = sum(1 for c in codes if c["used"])
        return {"total": len(codes), "unused": unused, "used": used}

    def next_unused(self) -> str | None:
        for c in self._load():
            if not c["used"]:
                return c["code"]
        return None

    def mark_used(self, code: str):
        codes = self._load()
        for c in codes:
            if c["code"] == code:
                c["used"] = True
        self._save(codes)

    def import_codes(self, raw_text: str):
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        codes = [{"code": l, "used": False} for l in lines]
        self._save(codes)
