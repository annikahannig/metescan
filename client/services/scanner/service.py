
"""
Scanner service
Handles scanner input, dispatches actions as needed.
"""

import sys
import asyncio

from services.scanner import actions


def input_stdin(dispatch):
    """Read data from stdin"""
    def reader():
        line = sys.stdin.readline()
        line = line.strip()
        dispatch(actions.input_barcode(line))
    return reader


@asyncio.coroutine
def main(dispatch, *args):
    """Scanner: Watch stdin"""
    loop = asyncio.get_event_loop()
    loop.add_reader(sys.stdin, input_stdin(dispatch))

