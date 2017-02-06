
"""
Store actions
"""

STORE_RESET = "@store/RESET"

STORE_ADD_PRODUCT = "@store/ADD_PRODUCT"
STORE_SET_ACCOUNT = "@store/SET_ACCOUNT"

STORE_CHECKOUT_START    = "@store/CHECKOUT_START"
STORE_CHECKOUT_COMPLETE = "@store/CHECKOUT_COMPLETE"


def reset_store():
    return {
        "type": STORE_RESET,
    }


def add_product(product):
    return {
        "type": STORE_ADD_PRODUCT,
        "payload": {
            "product": product,
        }
    }


def set_account(account):
    return {
        "type": STORE_SET_ACCOUNT,
        "payload": {
            "account": account
        }
    }



def start_checkout(account, cart):
    return {
        "type": STORE_CHECKOUT_START,
        "payload": {
            "account": account,
            "cart": cart,
        }
    }


def checkout_complete(result):
    return {
        "type": STORE_CHECKOUT_COMPLETE,
        "payload": {
            "result": result
        }
    }



