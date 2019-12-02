import random

from fut.exceptions import NoTradeExistingError

from src.utils.utils import sendMessage, sleep
from src.modules.fut.constants import TRADE_STATE_ACTIVE, WATCHLIST_SIZE, MAX_PAGE_FOR_SEARCH
import time


class Gold300Buyer:
    MAX_SEARCH_REQUESTS = 30
    MAX_OUTBID_THRESHOLD_PER_PAGE = 3
    MAX_BID_PRICE = 300

    def __init__(self, client):
        self.client = client

    def buy(self):
        client = self.client
        start = 0
        num_of_bids = 0
        ok = True
        num_requests = 0
        available_slots = WATCHLIST_SIZE - len(client.watchlist())

        print 'Available slots %d ' % available_slots
        while ok:
            if start >= MAX_PAGE_FOR_SEARCH:
                start = 0
                continue
            items = client.searchAuctions('player', level='gold', max_price=self.MAX_BID_PRICE, fast=True, start=start)
            items = items[::-1]  # Lets start bidding from the end to have better chance of beating Joe
            print 'Start Page %d ' % start
            items_length = len(items)
            start += items_length

            num_requests += 1
            falsy_counter = 0
            misses = 1
            for item in items:
                if available_slots <= 0:
                    ok = False
                    print 'No more slots on the watchlist, quitting'
                    break

                try:
                    trade_state = item['tradeState']
                    trade_id = item['tradeId']
                    if trade_state == TRADE_STATE_ACTIVE:
                        result = client.bid(trade_id, self.MAX_BID_PRICE)

                        if not result:
                            result = client.bid(trade_id, self.MAX_BID_PRICE + 50)
                        num_of_bids = num_of_bids + 1 if result else num_of_bids
                        available_slots = available_slots - 1 if result else available_slots
                        falsy_counter = falsy_counter + 1 if not result else falsy_counter
                        print '--> Bid: %d' % trade_id
                        print '--> Status: %s' % str(result)
                    else:
                        misses += 1

                    if falsy_counter >= self.MAX_OUTBID_THRESHOLD_PER_PAGE:
                        print '--> Skipping to next page because too many outbids\n'
                        break

                except NoTradeExistingError:
                    print 'NoTradeExistingError'
                    continue

            time_to_sleep = random.randint(1, 3)
            print('--> Sleeping for %d seconds before buying.' % time_to_sleep)
            # client.keepalive()
            sleep(time_to_sleep)

            if num_requests >= self.MAX_SEARCH_REQUESTS or misses == items_length:
                ok = False

        localtime = time.asctime(time.localtime(time.time()))
        msg = "Balance after bidding : %d %s" % (client.keepalive(), localtime)
        sendMessage(msg)
