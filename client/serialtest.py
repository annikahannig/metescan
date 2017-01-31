#!/usr/bin/env python3

import serial
import io

import asyncio

import time


def serial_init(device, baud_rate=19200):
    """Initialize serial interface"""
    ser = serial.Serial(device, 19200);
    return ser



def read_serial():
    """async read from serial io"""
    buf = ""
    res = s.read().decode()
    while res != '\n':
        buf += res

    print("RECV: {}".format(buf))



def main():

    ser = serial_init("/dev/tty.usbmodem1411", 19200)

    time.sleep(2)
    print("writing to serial")

    ser.write(bytes("0 Hallo\n", 'utf8'))
    time.sleep(0.1)
    ser.write(bytes("1 Display\n", 'utf8'))
    time.sleep(0.1)
    ser.write(bytes("2 Foo\n", 'utf8'))
    time.sleep(0.1)

    ser.write(b"HELO")

    loop = asyncio.get_event_loop()
    loop.add_reader(ser, read_serial)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()



if __name__ == '__main__':
    main()


