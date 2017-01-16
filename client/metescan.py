#!/usr/bin/env python3

import argparse
import asyncio
import sys

from mete import api, checkout

# Input goes here and will be evaluated in the
# app event loop.
INPUT_COMMAND = 0
INPUT_BARCODE = 1

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
    asyncio.async(input_queue.put((INPUT_BARCODE, line,)))


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
    # Initialize state
    account = None
    cart = []

    # Initialize client
    client = api.Client(args.mete_host, args.api_token)

    while True:
        input_type, input_data = yield from input_queue.get()
        if input_type == INPUT_COMMAND:
            return

        barcode = input_data
        print("[i] Fetching: {}".format(barcode))

        result_type, result, ok = client.retrieve_barcode(barcode)
        if not ok:
            print("[e] Unknown barcode")
            continue

        if result_type == api.RESULT_ACCOUNT:
            account = result
            print("[+] Hello {username}".format(**account))
        else:
            product = result
            cart.append(result)
            print("[+] {name} for {price}".format(**product))

        # Can we do a purchase?
        if checkout.is_available(account, cart):
            result = checkout.perform(client, account, cart)
            print("[i] All done. New balance: {}".format(result['new_balance']))
            # Print new account stats
            # Reset
            account = None
            cart = []


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
