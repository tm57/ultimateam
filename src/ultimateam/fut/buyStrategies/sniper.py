from src.utils.utils import log, sleep


class Sniper:
    MAX_MISSES = 3

    def __init__(self, client):
        self.client = client

    def buy(self):
        client = self.client
        ok = True
        start = 0
        bid = 850
        won_items = []

        available_slots = len(self.client.unassigned())
        while ok:
            items = client.searchAuctions('development', max_buy=bid, defId=5002006, fast=False, start=start)
            items = items[::-1]
            if not len(items):
                print('No items dawg')
                start = 0
                continue

            start = start + len(items)
            miss = 0
            for item in items:

                state = client.bid(item['tradeId'], bid)
                if state:
                    won_items.append(item['tradeId'])
                    data = '%d, %d \n' % (bid, item['tradeId'])
                    log(data, filename='./data/sniper.csv')
                    print('Snipped %d for %d' % (item['tradeId'], bid))
                    available_slots -= 1
                else:
                    print('Lost it')
                    bid = 900
                    miss += 1
                if miss > self.MAX_MISSES:
                    start += len(items)
                    bid = 850
                    break

                if len(won_items) >= 50 or available_slots <= 50:
                    ok = False
                    break
            print('Still running')
            # self.client.keepalive()
            sleep(3)
