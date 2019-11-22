class SniperSellerRule:
    def __init__(self, bid_price, buy_now_price, duration=3600):
        self.bid_price = bid_price
        self.buy_now_price = buy_now_price
        self.duration = duration
