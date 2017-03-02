
"""
Mete Idle Mode
"""

import asyncio

from mete import api
from datetime import datetime

from services.store import actions as store_actions
from services.display import actions as display_actions
from services.scanner import actions as scanner_actions
from services.idle_watchdog import actions as idle_actions

class StatusScreen(object):
    """Show some mete stats"""

    def __init__(self, client, args):
        """Initialize status screen"""
        self.args = args
        self.client = client

        self.enabled = True # Initial state
        self.stats = None


    @asyncio.coroutine
    def _fetch_stats(self):
        """Fetch stats from server"""
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, self.client.stats)
        yield from future
        self.stats, ok = future.result()

    @asyncio.coroutine
    def _update_stats(self):
        """Update statistics periodically"""
        while True:
            yield from self._fetch_stats()
            yield from asyncio.sleep(30)


    @asyncio.coroutine
    def _display_stats(self):
        """Async display loop"""
        while True:
            if not self.enabled:
                yield from asyncio.sleep(0.2)
                continue

            # Update Display with info
            buf = []
            now = datetime.now()
            stats = self.stats
            if stats:
                buf = [
                    "Mete {0: >15}".format(stats['backend_version']),
                    "TX this month: {0: >5}".format(
                        stats['transactions']['current_month']),
                    "Users: {0: >13}".format(stats['users']),
                    now.strftime("%d.%m.%Y  %H:%M:%S")
                ]

            else:
                buf = [
                    "MeteScan",
                    "",
                    self.args.mete_host[:20],
                    self.args.mete_host[20:]
                ]

            # Push buffer
            for i, line in enumerate(buf):
                self.dispatch(display_actions.set_line(i, line))

            # Wait
            yield from asyncio.sleep(1)


    @asyncio.coroutine
    def main(self, dispatch, queue):
        """Idle display screensaver"""

        self.dispatch = dispatch

        asyncio.async(self._display_stats())
        asyncio.async(self._update_stats())

        while True:
            action = yield from queue.get()
            if action['type'] == scanner_actions.INPUT_BARCODE:
                self.enabled = False
            elif action['type'] == idle_actions.IDLE_TIMEOUT:
                self.enabled = True
            elif action['type'] == display_actions.BUTTON_CANCEL_PRESSED:
                self.enabled = True
            elif action['type'] == store_actions.STORE_CHECKOUT_COMPLETE:
                asyncio.async(self._fetch_stats())

