import asyncio
import random
import time


class Seller:

    def __init__(self, seller, client):

        self.client = client
        self.seller = seller

    async def sell(self, item_ids):
        trade_ids = []
        self.client.keepalive()
        if not item_ids:
            print('--> Trade ids need to be provided for a sale to proceed')
            return

        for item_id in item_ids:
            if not item_id:
                print('This is invalid %d ' % item_id)
                continue
            trade_id = self.seller.sell(item_id)
            trade_ids.append(trade_id)

            time_to_sleep = random.randint(7, 26)
            print('--> Sleeping for %d seconds before selling.' % time_to_sleep)
            await asyncio.sleep(time_to_sleep)
        return trade_ids
