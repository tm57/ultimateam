import asyncio
from random import random


class Exchanger:
    STEP = 100
    SLEEP_TIME_RANGE = [1, 5]
    whitelist = [
        'quantity',
        'excess_value',
        'type',
        'max_buy',
        'max_price',
        'trade_ids',
        'level'
    ]

    def __init__(self, client, **kwargs):
        self.quantity = 0
        self.trade_ids = []
        self.max_buy = None
        self.max_price = None
        self.level = None
        self.type = None
        self.client = client
        self.num_bids_placed = 0

        for key, value in kwargs.items():
            if key in self.whitelist:
                setattr(self, key, value)

    def buy(self):
        if self.trade_ids:
            return self._performTargetItemsHunt()
        return self._performUptoHunt()

    async def _performUptoHunt(self):
        start = 0
        client = self.client
        ok = True

        while ok:
            items = client.searchAuctions(self.type, level=self.level, max_buy=self.max_buy, max_price=self.max_price,
                                          fast=False,
                                          start=start)
            for item in items:
                trade_id = item['tradeId']
                state = self._bidUpto(trade_id, self.max_price, self.max_buy)
                if state:
                    self.num_bids_placed += 1
                    if self.num_bids_placed >= self.quantity:
                        ok = False
                        break
            if ok:
                time_to_sleep = random.randint(*self.SLEEP_TIME_RANGE)
                print(f'Awaiting for {time_to_sleep} seconds before bidding')
                await asyncio.sleep(time_to_sleep)
            if not len(items):
                ok = False
            start += len(items)
        return self.num_bids_placed

    def _bidUpto(self, trade_id, start, max_buy):
        end = max_buy + self.STEP
        for bid in range(start, end, self.STEP):
            state = self.client.bid(trade_id, bid)
            if not state:
                continue
            else:
                return state

        return False

    async def _performTargetItemsHunt(self):
        client = self.client
        start = 0
        ok = True
        found = 0
        while ok:
            items = client.searchAuctions(self.type, level=self.level, max_buy=self.max_buy,
                                          max_price=self.max_price, fast=True,
                                          start=start)
            time_to_sleep = random.randint(*self.SLEEP_TIME_RANGE)
            await asyncio.sleep(time_to_sleep)
            my_targets = filter(lambda item: item['tradeId'] in self.items, items)
            if not my_targets:
                print(f'Awaiting for {time_to_sleep} seconds before bidding, there were no targets found on this page')
                continue

            for target in my_targets:
                state = client.bid(target['tradeId'], self.max_buy)
                if state:
                    found += 1
                if found == self.quantity:
                    ok = False
                    print('Found All Items')
                    break

            if not len(items):
                ok = False
            start += len(items)
        return found
