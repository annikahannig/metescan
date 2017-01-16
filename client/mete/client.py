
import requests

def retrieve_barcode(host, token, barcode):
    """Fetch associated object from server"""
    url = "{}/api/barcode/{}/".format(host, barcode)
    res = requests.get(url, headers={
        'Authorization': 'Token {}'.format(token)
    })

    return (res.json(), res.status_code == 200)

def is_account(obj):
  """Check if response is account"""
  if obj.get('username'):
    return True
  return False

