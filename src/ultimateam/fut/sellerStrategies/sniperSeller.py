class SniperSeller:

    def __init__(self, client, sniper_sell_rule):
        self.sniper_sell_rule = sniper_sell_rule
        self.client = client

    def sell(self, trade_id):
        sniper_sell_rule = self.sniper_sell_rule

        self.client.sell(
            trade_id,
            sniper_sell_rule.bid_price,
            buy_now=sniper_sell_rule.buy_now_price,
            duration=sniper_sell_rule.duration
        )
