"""
Store Main Service
Handle transactions and main app logic

"""

import asyncio

from services.display import actions as display_actions
from services.store import actions as store_actions
from services.scanner import actions as scanner_actions
from services.barcode_decoder import actions as decoder_actions
from services.idle_watchdog import actions as idle_actions

from mete import api, checkout

class Store(object):
    """Metestore"""

    def __init__(self, args):
        """Setup store, get settings from args"""
        self.args = args
        self.reset()

        # Initialize client
        self.client = api.Client(args.mete_host,
                                 args.api_token)

        self.locked = False


    def reset(self):
        """Reset store"""
        self.in_progress = False
        self.locked = False
        self.account = None
        self.cart = []


    def clear_on_first_scan(self):
        """Clear display, start shopping"""
        if self.in_progress:
            return

        self.dispatch(display_actions.clear())
        self.in_progress = True


    def add_product(self, product):
        """Handle incoming product"""
        if self.locked:
            return

        self.cart.append(product)

        # Update display
        padding = 20 - len(product['name']) - 1
        prod_text = "{0} {1: >{2}}".format(product['name'],
                                           product['price'],
                                           padding)
        self.dispatch(display_actions.add_line(prod_text))

        # Can we finish our transaction?
        if checkout.is_available(self.account, self.cart):
            self.checkout_cart()


    def set_account(self, account):
        """Handle incoming account"""
        if self.locked:
            return

        self.account = account

        # Update display
        text = "Hallo {}!".format(account['username'])
        self.dispatch(display_actions.add_line(text))
        key = "Konto:"
        text = "{0} {1: >{2}}".format(key,
                                     account['account']['balance'],
                                     20 - len(key) - 1)
        self.dispatch(display_actions.add_line(text))


        # Can we finish our transaction?
        if checkout.is_available(self.account, self.cart):
            self.checkout_cart()


    def checkout_cart(self):
        """Perform checkout"""
        self.locked = True # Sleep a bit before next user
        self.dispatch(store_actions.start_checkout(self.account,
                                                   self.cart))

        result = checkout.perform(self.client,
                                  self.account,
                                  self.cart)

        # Update display
        key = "Neu:"
        text = "{0} {1: >{2}}".format(key,
                                     result['new_balance'],
                                     20 - len(key) - 1)
        self.dispatch(display_actions.add_line(text))

        # Inform all, that the transaction is finished
        self.dispatch(store_actions.checkout_complete(result))


    def barcode_error(self):
        """In case an invalid barcode was supplied"""
        self.dispatch(display_actions.add_line("Barcode unbekannt"))


    # Metestore Main
    @asyncio.coroutine
    def main(self, dispatch, queue):
        """Initialize metestore, handle actions"""

        print("Starting Metestore")
        self.dispatch = dispatch

        # Initialize state
        account = None
        cart = []

        # Initialize client
        client = api.Client(self.args.mete_host,
                            self.args.api_token)

        # Main event loop
        while True:
            action = yield from queue.get()

            if action['type'] == store_actions.STORE_RESET:
                self.reset()
            elif action['type'] == store_actions.STORE_CHECKOUT_COMPLETE:
                self.reset()
            elif action['type'] == idle_actions.IDLE_TIMEOUT:
                self.reset()
            elif action['type'] == decoder_actions.DECODED_PRODUCT:
                self.add_product(action['payload']['product'])
            elif action['type'] == decoder_actions.DECODED_ACCOUNT:
                self.set_account(action['payload']['account'])
            elif action['type'] == decoder_actions.DECODING_ERROR:
                self.barcode_error()
            elif action['type'] == scanner_actions.INPUT_BARCODE:
                self.clear_on_first_scan()



