import os

import fut


class FutClient:

    def __init__(self, email, password, passphrase, platform='ps4', code=None):
        debug = os.getenv('APP_ENV') == 'development'
        self.client = fut.Core(email, password, passphrase,
                               platform=platform,
                               code=code,
                               debug=debug,
                               cookies='auth/' + passphrase + '_cookie.txt', token='auth/' + passphrase + '_token.txt')

    def getClient(self):
        return self.client
