"""
Store Main Service
Handle transactions and main app logic

"""

import asyncio

from services.store import actions as store_actions
from services.barcode_decoder import actions as decoder_actions

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


    def reset(self):
        """Reset store"""
        self.account = None
        self.cart = []


    def add_product(self, product):
        """Handle incoming product"""
        self.cart.append(product)
        # Update display

        # Can we finish our transaction?
        if checkout.is_available(self.account, self.cart):
            self.checkout_cart()


    def set_account(self, account):
        self.account = account
        # Update display

        # Can we finish our transaction?
        if checkout.is_available(self.account, self.cart):
            self.checkout_cart()


    def checkout_cart(self):
        """Perform checkout"""
        self.dispatch(store_actions.start_checkout(self.account,
                                                   self.cart))

        result = checkout.perform(self.client,
                                  self.account,
                                  self.cart)

        self.dispatch(store_actions.checkout_complete(result))


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
            elif action['type'] == decoder_actions.DECODED_PRODUCT:
                self.add_product(action['payload']['product'])
            elif action['type'] == decoder_actions.DECODED_ACCOUNT:
                self.set_account(action['payload']['account'])
            elif action['type'] == store_actions.STORE_CHECKOUT_COMPLETE:
                self.reset()



