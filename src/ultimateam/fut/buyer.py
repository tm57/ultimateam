class Buyer:
    def __init__(self, buy_strategy):
        self.buyStrategy = buy_strategy

    def buy(self):
        self.buyStrategy.buy()
