#!/usr/bin/env python3

"""
Metescan
"""

import asyncio
import argparse

from aflow import dispatchers

# Async services
from services.scanner import service as scanner_service
from services.barcode_decoder import service as decoder_service
from services.store import service as store_service

from services.display_emulation import service as display_emu_service


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

    # Setup Services
    store = store_service.Store(args)
    decoder = decoder_service.BarcodeDecoder(args)
    display_emulation = display_emu_service.DisplayEmulation("./mete.disp")


    # Setup application
    loop = asyncio.get_event_loop()

    dispatcher = dispatchers.ActionDispatcher(debug=True)

    dispatcher.connect(scanner_service.main)
    dispatcher.connect(decoder.main)
    dispatcher.connect(store.main)
    dispatcher.connect(display_emulation.main)

    loop.run_forever()



if __name__ == '__main__':
    main()


