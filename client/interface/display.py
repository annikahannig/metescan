
"""
Display Interface
-----------------

Handle serial connection and button events

"""

import asyncio
import serial


CMD_KEYPRESS = 0
CMD_SET_LINE = 1
CMD_IDLE_MODE = 2


_cmd_queue = asyncio.Queue()


def set_line(line, text):
    """Enqueue display command: set line"""
    print("set line called: {} {}".format(line, text))
    _cmd_queue.put((CMD_SET_LINE, (line, text)))


async def _display_set_line(ser, line, text):
    """Write line to display"""
    ser.write("{} {}\n".format(line, text[:20]))
    print("{} {}\n".format(line, text[:20]))
    await asyncio.sleep(0.1)


@asyncio.coroutine
def display_main(args):
    """
    Display control routine
    """
    print("[i] Initializing interface at {}".format(args.device))
    ser = serial.Serial(args.device, args.baud_rate);

    # Wait at least 2 seconds before writing to serial
    yield from asyncio.sleep(2)

    while True:
        cmd, payload = yield from _cmd_queue.get()
        if cmd == CMD_KEYPRESS:
            print("Display key Pressed: {}".format(payload))
        elif cmd == CMD_SET_LINE:
            _display_set_line(ser, *payload)

