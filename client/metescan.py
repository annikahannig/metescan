#!/usr/bin/env python3

"""
Metescan
"""

import asyncio
import argparse

from aflow import dispatchers

from mete import api

# Async services
from services.scanner import service as scanner_service
from services.barcode_decoder import service as decoder_service
from services.store import service as store_service
from services.status_screen import service as status_service
from services.idle_watchdog import service as idle_service
from services.display import service as display_service

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

    # Initialize client
    client = api.Client(args.mete_host,
                        verify=args.verify_ca_bundle,
                        token=args.api_token)

    # Setup Services
    store = store_service.Store(client, args)
    decoder = decoder_service.BarcodeDecoder(client, args)
    status_screen = status_service.StatusScreen(client, args)
    watchdog = idle_service.Watchdog(timeout=15)

    display = display_service.SerialDisplay(args.device, args.baud_rate)
    display_emulation = display_emu_service.DisplayEmulation("./mete.disp")

    # Setup application
    loop = asyncio.get_event_loop()

    dispatcher = dispatchers.ActionDispatcher(debug=False)

    dispatcher.connect(scanner_service.main)
    dispatcher.connect(decoder.main)
    dispatcher.connect(store.main)
    dispatcher.connect(status_screen.main)
    dispatcher.connect(watchdog.main)
    dispatcher.connect(display.main)
    dispatcher.connect(display_emulation.main)

    loop.run_forever()


if __name__ == '__main__':
    main()


