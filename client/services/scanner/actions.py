
"""
Barcode Scanner Actions
"""

INPUT_BARCODE = '@scanner/INPUT_BARCODE'

def input_barcode(code):
    return {
        'type': INPUT_BARCODE,
        'payload': {
            'barcode': code
        }
    }


