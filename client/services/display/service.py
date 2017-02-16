
"""
Display Service
Communicate with display using serialio.

Receives display actions,
emits button press actions.
"""

import serial
import io

import asyncio
from copy import copy

from services.display import actions as display_actions

class SerialDisplay(object):
    """Display at serial line"""

    def __init__(self, device, baud_rate):
        """Initialize serial connection"""
        self.serial = serial.Serial(device, baud_rate)

        # TODO: Make this configurable
        self.rows = 4
        self.cols = 20

        # Initialize buffer
        self.buf = [" " * self.cols for _ in range(self.rows)]
        self.diff_buf = copy(self.buf)

        self.dispatch = False

        loop = asyncio.get_event_loop()
        loop.add_reader(self.serial, self._read_serial_input)

    def _clear(self):
        """Clear screen"""
        self.buf = [" " * self.cols for _ in range(self.rows)]


    def _add_line(self, line):
        """Add line to buffer"""
        self.buf.append(line)
        self.buf = self.buf[-self.rows:] # limit buffer size


    def _set_line(self, i, line):
        """Set line on display"""
        self.buf[i] = line


    def _read_serial_input(self):
        """Async reader from serial"""
        if not self.dispatch:
            return

        line = ""
        res = ""
        while res != '\n' and res != '\r':
           res = self.serial.read().decode()
           line += res
        line = line.strip()
        if line == 'BT_CANCEL_UP':
            self.dispatch(display_actions.button_cancel_pressed())

    @asyncio.coroutine
    def _write_buffer(self):
        """Write buffer to serial display"""
        diff = []
        screen = [row[:self.cols] for row in self.buf]

        # Make diff, only transmit lines with changes
        for i, row in enumerate(screen):
            if row != self.diff_buf[i]:
                diff.append((i, row))

        for row, update in diff:
            update += " " * (20 - len(update)) # fill with blanks
            data = "{} {}\n".format(row, update)
            # padup data to clear line
            self.serial.write(bytes(data, 'utf8'))
            yield from asyncio.sleep(0.05)

        self.diff_buf = screen

    @asyncio.coroutine
    def _update_display(self):
        """Update display loop"""
        while True:
            yield from self._write_buffer()
            yield from asyncio.sleep(0.1)


    @asyncio.coroutine
    def main(self, dispatch, queue):
        """Serial communication service"""
        self.dispatch = dispatch

        # Wait after powerup
        yield from asyncio.sleep(1)

        # Update screen
        asyncio.ensure_future(self._update_display())

        while True:
            action = yield from queue.get()

            if action['type'] == display_actions.CLEAR:
                self._clear()

            elif action['type'] == display_actions.ADD_LINE:
                self._add_line(action['payload']['line'])

            elif action['type'] == display_actions.SET_LINE:
                self._set_line(action['payload']['index'],
                               action['payload']['line'])

