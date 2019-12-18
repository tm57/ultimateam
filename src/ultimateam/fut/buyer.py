class Buyer:
    def __init__(self, buy_strategy, **kwargs):
        self.buyStrategy = buy_strategy(**kwargs)

    def buy(self):
        self.buyStrategy.buy()
