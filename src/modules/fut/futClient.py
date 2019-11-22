import os
import fut


class FutClient:

    def __init__(self, platform='ps4'):
        self.client = fut.Core(os.getenv('FUT_EMAIL'),
                               os.getenv('FUT_PASSWORD'),
                               os.getenv('FUT_PASSPHRASE'),
                               platform=platform)

    def getClient(self):
        return self.client
