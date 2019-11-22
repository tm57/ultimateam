from src.utils.utils import log


class Sniper:
    def __init__(self, client):
        self.client = client

    def buy(self):
        client = self.client
        ok = True
        start = 0
        bid = 800
        won_items = []
        while ok:
            items = client.searchAuctions('development', max_buy=bid, defId=5002006, fast=False, start=start)

            if not len(items):
                break

            start = start + len(items)
            for item in items:

                state = client.bid(item['tradeId'], bid)
                if state:
                    won_items.append(item['tradeId'])
                    data = '%d, %d \n' % (bid, item['tradeId'])
                    log(data, filename='./data/sniper.csv')
                    print 'Snipped %d for %d' % (item['tradeId'], bid)
                else:
                    print 'Lost it'
                    # bid = 750

                if len(won_items) >= 10:
                    ok = False
                    break
            print 'Still running'
