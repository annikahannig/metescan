

import asyncio

from services.scanner import actions as scanner_actions
from services.barcode_decoder import actions as decoder_actions

from mete import api



class BarcodeDecoder(object):
    """Decode incoming barcodes, emits products and accounts"""

    def __init__(self, client, args):
        """Initialize decoder"""
        self.args = args

        # Initialize client
        self.client = client


    def handle_barcode(self, barcode):
        """Process an incomming barcode"""
        if barcode == "":
            return # Don't bother

        result_type, result, ok = self.client.retrieve_barcode(barcode)
        if not ok:
            self.dispatch(decoder_actions.error_decoding("Unknown Barcode"))
            return

        if result_type == api.RESULT_ACCOUNT:
            self.dispatch(decoder_actions.account_decoded(result))
        else:
            self.dispatch(decoder_actions.product_decoded(result))


    @asyncio.coroutine
    def main(self, dispatch, queue):
        """Run Barcode decoder"""
        self.dispatch = dispatch

        while True:
            action = yield from queue.get()
            if action['type'] == scanner_actions.INPUT_BARCODE:
                self.handle_barcode(action['payload']['barcode'])

