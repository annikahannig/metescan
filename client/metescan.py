#!/usr/bin/env python3

"""
Metescan
"""

import asyncio
import argparse

from aflow import dispatchers

# Async services
from services.scanner import service as scanner_service
from services.store import service as store_service


def parse_arguments():
    """Get commandline arguments"""
    parser = argparse.ArgumentParser(description='Scantool Params')
    parser.add_argument('-t', '--api-token', required=True)
    parser.add_argument('-m', '--mete-host', required=True)
    parser.add_argument('-c', '--verify-ca-bundle', default=True)
    parser.add_argument('-d', '--device', required=True)
    parser.add_argument('-b', '--baud-rate', default=19200)

    return parser.parse_args()


def main():
    """Start scan and checkout"""

    # Get commandline params
    args = parse_arguments()

    # Setup Metestore
    store = store_service.Store(args)

    loop = asyncio.get_event_loop()

    # Setup application
    dispatcher = dispatchers.ActionDispatcher(debug=True)
    dispatcher.connect(scanner_service.main)
    dispatcher.connect(store.main)

    loop.run_forever()



if __name__ == '__main__':
    main()


