import requests

# Constants
RESULT_BARCODE = 0
RESULT_ACCOUNT = 1


class Client(object):

    def __init__(self, host, token, verify=False):
        self.host = host
        self.token = token
        self.verify = verify

        # Don't do this in production!
        if not self.host.startswith('https'):
            print("[WARNING] --------------------------------------------")
            print("[WARNING] CONNECTING VIA UNSAFE HTTP!")
            print("[WARNING] F O R  T E S T I N G  P U R P O S E  O N L Y")
            print("[WARNING] --------------------------------------------")

    def is_account(self, obj):
        """Check if response is account"""
        if obj.get('username'):
            return True
        return False


    def retrieve_barcode(self, barcode):
        """Fetch associated object from server"""
        url = "{}/api/barcode/{}/".format(self.host, barcode)
        res = requests.get(url, verify=self.verify, headers={
            'Authorization': 'Token {}'.format(self.token)
        })

        obj = res.json()

        # Check object associated to barcode
        result_type = RESULT_BARCODE
        if self.is_account(obj):
            result_type = RESULT_ACCOUNT

        return (result_type, obj, res.status_code == 200)


    def purchase(self, account, product):
        """Perform purchase, returns updated account"""
        url = "{}/api/users/{}/purchase/".format(self.host, account['id'])
        payload = {
            "product": product['id'],
        }

        # Perform purchase
        res = requests.post(url, payload, verify=self.verify, headers={
            'Authorization': 'Token {}'.format(self.token)
        })

        return (res.json(), res.status_code == 200)


    def stats(self):
        """Get some statistics from mete server"""
        url = "{}/api/stats/".format(self.host)
        res = requests.get(url)
        return (res.json(), res.status_code == 200)
