

"""
Barcode decoder
"""

DECODING_BEGIN = "@barcode_decoder/DECODING_BEGIN"
DECODING_ERROR = "@barcode_decoder/DECODING_ERROR"

DECODED_ACCOUNT = "@barcode_decoder/DECODED_ACCOUNT"
DECODED_PRODUCT = "@barcode_decoder/DECODED_PRODUCT"


# Action creators
def begin_decoding(barcode):
    return {
        "type": DECODING_BEGIN,
        "payload": {
            "barcode": barcode,
        },
    }


def error_decoding(err):
    return {
        "type": DECODING_ERROR,
        "payload": {
            "error": err
        }
    }


def account_decoded(account):
    return {
        "type": DECODED_ACCOUNT,
        "payload": {
            "account": account,
        },
    }


def product_decoded(product):
    return {
        "type": DECODED_PRODUCT,
        "payload": {
            "product": product,
        },
    }

