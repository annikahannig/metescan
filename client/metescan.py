#!/usr/bin/env python3

import argparse
import asyncio
import sys

from mete import client

# Input goes here and will be evaluated in the
# app event loop.
input_queue = asyncio.Queue()

def parse_arguments():
    """Get commandline arguments"""
    parser = argparse.ArgumentParser(description='Scantool Params')
    parser.add_argument('-t', '--api-token', required=True)
    parser.add_argument('-m', '--mete-host', required=True)

    return parser.parse_args()


# Readers
def input_stdin():
    """Read from STDIN (Scanner)"""
    line = sys.stdin.readline()
    asyncio.async(input_queue.put(('barcode', line,)))


def input_serial():
    """Read commands from serial (Keys)"""
    print("Read.")


# Application Main
@asyncio.coroutine
def app_main(args):
    """
    Main application loop:
    Process input, make requests.
    """

    cart = []


    while True:
        input_type, input_data = yield from input_queue.get()
        if input_type == 'command':
            return

        barcode = input_data
        print("[i] Fetching: {}".format(barcode))

        result, ok = client.retrieve_barcode(args.mete_host,
                                             args.api_token,
                                             barcode)
        if not ok:
            print("[e] Unknown barcode")
            continue

        if client.is_account(result):
            account = result
            print("[+] Hello {username}".format(**account))
        else:
            product = result
            print("[+] Checkout {name} for {price}".format(**product))


def main():
    """Initialize and start event loop"""

    # Get commandline params
    args = parse_arguments()

    loop = asyncio.get_event_loop()

    # Listen for input 
    loop.add_reader(sys.stdin, input_stdin)

    # Start app
    loop.run_until_complete(app_main(args))


if __name__ == '__main__':
    main()
