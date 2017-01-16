
"""
Mete Cart Checkout
------------------

Perform purchase
"""


def total_amount(cart):
    """Get total amount of products"""
    return 0

def is_available(account, cart):
    """Can we perform a checkout?"""
    return account and len(cart) > 0


def perform(client, account, cart):
    """Get items from cart, bill to account using client instance"""
    print("[i] Performing checkout for {username}".format(**account))
    for item in cart:
        print("[+]   {name} for {price}".format(**item))

