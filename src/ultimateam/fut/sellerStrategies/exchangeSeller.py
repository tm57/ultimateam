class ExchangeSeller:
    def __init__(self, client, policy):
        self.policy = policy
        self.client = client

    def sell(self, trade_id):
        self.client.sell(trade_id, **self.policy)
