"""
Display Emulation
Writes display to file
"""

import asyncio

from services.display import actions as display_actions

class DisplayEmulation(object):

    def __init__(self, filename, rows=4, cols=20):
        """Initializes display emulation"""
        self.filename = filename
        self.rows = rows
        self.cols = cols

        self.buf = None # Display linebuffer
        self._clear()


    def _clear(self):
        """Clears buffer"""
        # Make sure we have always at least
        # a whole set of rows 
        self.buf = ["" for _ in range(self.rows)]
        self._write_buffer()


    def _add_line(self, line):
        """Add line to buffer"""
        self.buf.append(line)
        self._write_buffer()


    def _set_line(self, i, line):
        """Set line relative to view port"""
        offset = min(0, len(self.buf) - self.rows)
        self.buf[offset + i] = line
        self._write_buffer()


    def _write_buffer(self):
        """Write buffer to file"""
        screen = [row[:self.cols] for row in self.buf[-self.rows:]]
        with open(self.filename, "w+") as f:
            f.write("-----[Display]------\n")
            f.write("\n".join(screen))
            f.write("\n--------------------")


    @asyncio.coroutine
    def main(self, dispatch, queue):
        """Service main loop"""

        while True:
            action = yield from queue.get()

            if action['type'] == display_actions.CLEAR:
                self._clear()

            elif action['type'] == display_actions.ADD_LINE:
                self._add_line(action['payload']['line'])

            elif action['type'] == display_actions.SET_LINE:
                self._set_line(action['payload']['index'],
                               action['payload']['line'])


