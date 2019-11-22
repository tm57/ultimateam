class Gold300Seller:
    BID_PRICE = 450

    BUY_NOW_PRICE = 500

    def __init__(self, client):
        self.client = client

    def sell(self, trade_id):
        self.client.sell(trade_id, self.BID_PRICE, buy_now=self.BUY_NOW_PRICE, duration=3600)
