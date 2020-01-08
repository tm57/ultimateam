class ExchangeSellerPolicy:

    @staticmethod
    def get():
        return {
            'max_price': 2500,
            'max_buy': 7000,
            'duration': 3600 * 24
        }
