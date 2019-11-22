import random
import time


class Seller:

    def __init__(self, seller, client):

        self.client = client
        self.seller = seller

    def sell(self, item_ids):

        if not item_ids:
            print '--> Trade ids need to be provided for a sale to proceed'
            return

        for item_id in item_ids:
            if not item_id:
                print 'This is invalid %d ' % item_id
                continue
            self.seller.sell(item_id)

            time_to_sleep = random.randint(13, 26)
            print('--> Sleeping for %d seconds before selling.' % time_to_sleep)
            time.sleep(time_to_sleep)
