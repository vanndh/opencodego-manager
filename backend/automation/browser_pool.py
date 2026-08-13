"""Browser pool — bounded concurrency contexts.

Не запускаем десятки браузеров. Pool + semaphore: берём контекст на
операцию (login / bonus / api), возвращаем после.
"""

import asyncio
import contextlib


class BrowserPool:
    def __init__(self, max_browsers: int = 3):
        self._sem = asyncio.Semaphore(max_browsers)
        self._browser = None

    @contextlib.asynccontextmanager
    async def acquire(self):
        async with self._sem:
            browser = await self._ensure_browser()
            ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
            try:
                yield ctx
            finally:
                await ctx.close()

    async def _ensure_browser(self):
        if self._browser is None:
            from playwright.async_api import async_playwright
            self._pw = await async_playwright().start()
            self._browser = await self._pw.chromium.launch(
                headless=True, args=["--disable-blink-features=AutomationControlled"]
            )
        return self._browser

    async def close(self):
        if self._browser:
            await self._browser.close()
            self._browser = None
        if getattr(self, "_pw", None):
            await self._pw.stop()
            self._pw = None
