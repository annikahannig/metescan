
"""
Mete Idle Mode
"""

import asyncio

from mete import api
from interface import display
from datetime import datetime

_stats = none
_enabled = false

def enable():
    _enabled = True

def disable():
    _enabled = False


def _fetch_stats(client):
    """Fetch statistics using a mete client"""
    print("[i] Updating statistics...")
    _stats = client.stats()


@asyncio.coroutine
def _update_stats(client):
    while True:
        _fetch_stats(client)
        yield from asyncio.sleep(30)



@asyncio.coroutine
def idle_main(args):
    """Idle display screensaver"""
    client = api.Client(args.mete_host, args.api_token)
    asyncio.ensure_future(_update_stats(client))

    while True:
        print("idle loop: ".format(_enabled))
        if not _enabled:
            yield from asyncio.sleep(0.5)
            continue

        # Update Display with info
        buf = []
        now = datetime.now()
        if _stats:
            buf = [
                "Welcome to Mete {}".format(stats['backend_version']),
                "Transactions this month: {}".format(
                    stats['transactions']['current_month']),
                "Users: {}".format('users'),
                "          {}".format(now.strftime("%h:%m:%s %d.%m.%Y"))
            ]
        # Push buffer
        for i, line in enumerate(buf):
            display.set_line(i, line)

        # Wait
        yield from asyncio.sleep(1)
