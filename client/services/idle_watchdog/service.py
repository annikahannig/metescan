
"""
Idle watchdog
"""

import asyncio

from services.scanner import actions as scanner_actions
from services.idle_watchdog import actions as idle_actions

class Watchdog(object):

    def __init__(self, timeout):
        self.timeout = timeout
        self.time = 0


    async def _run_timer(self):
        """Run async timer"""
        while True:
            await asyncio.sleep(1)
            self.time += 1

            if self.time >= self.timeout:
                self.dispatch(idle_actions.idle_timeout())
                self.time = 0



    @asyncio.coroutine
    def main(self, dispatch, queue):
        """
        Process input, if nothing happens within timout,
        dispatch idle timeout action
        """
        self.dispatch = dispatch # i'll need to fix this
        asyncio.ensure_future(self._run_timer())

        while True:
            action = yield from queue.get()

            if action['type'] == scanner_actions.INPUT_BARCODE:
                self.time = 0


