import os
import fut


class FutClient:

    def __init__(self, platform='ps4'):
        passphrase = os.getenv('FUT_PASSPHRASE')
        self.client = fut.Core(os.getenv('FUT_EMAIL'),
                               os.getenv('FUT_PASSWORD'),
                               passphrase,
                               platform=platform,
                               cookies='auth/' + passphrase + '_cookie.txt',
                               token='auth/' + passphrase + '_token.txt')

    def getClient(self):
        return self.client
