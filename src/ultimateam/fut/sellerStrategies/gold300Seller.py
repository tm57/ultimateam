class Gold300Seller:
    BID_PRICE = 450

    BUY_NOW_PRICE = 550

    def __init__(self, client):
        self.client = client

    def sell(self, trade_id):
        # Trying to spread the items across time
        # I have noticed that the sell usually goes through at the end of the expiry time

        duration = 3600 if trade_id % 2 == 0 else 3600 * 3
        self.client.sell(trade_id, self.BID_PRICE, buy_now=self.BUY_NOW_PRICE, duration=duration)
