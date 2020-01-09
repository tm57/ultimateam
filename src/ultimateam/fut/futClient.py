import fut


class FutClient:

    def __init__(self, email, password, passphrase, platform='ps4', code=None):
        self.client = fut.Core(email, password, passphrase,
                               platform=platform,
                               code=code,
                               cookies='auth/' + passphrase + '_cookie.txt', token='auth/' + passphrase + '_token.txt')

    def getClient(self):
        return self.client
