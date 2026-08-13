"""Единая точка конфигурации приложения.

Имя, версия, автор — здесь, читаются backend'ом и frontend'ом.
"""

from pathlib import Path

APP_NAME = "OpenCode GO Manager"
APP_SLUG = "opengom"
APP_VERSION = "0.1.0"
APP_AUTHOR = "vanndh"

BACKEND_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BACKEND_DIR.parent
DATA_DIR = ROOT_DIR / "data"
FRONTEND_DIST = ROOT_DIR / "frontend" / "dist"

DB_PATH = DATA_DIR / "opengom.db"
VAULT_PATH = DATA_DIR / "vault.bin"

# Основной backend API (web UI)
API_HOST = "127.0.0.1"
API_PORT = 8080

# Локальный gateway (отдельный порт)
GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 3456

# По умолчанию: поднимать UI в браузере при старте
LAUNCH_BROWSER = True
