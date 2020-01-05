class Buyer:
    def __init__(self, buy_strategy):
        self.buyStrategy = buy_strategy

    async def buy(self):
        await self.buyStrategy.buy()
