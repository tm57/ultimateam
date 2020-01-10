from flask import jsonify

from src.ultimateam.TransferMarketManager import TransferMarketManager


class TradingController:
    def __init__(self, request):
        self.request = request

    def run(self):
        data = self.request.get_json()

        action = data['action']
        manager = TransferMarketManager(data['email'], data['password'], data['passphrase'], data['codes'])

        if action == 'buy':
            manager.performBuy(data['strategy'])
        elif action == 'sell':
            manager.performSell(data['strategy'])
        elif action == 'auto':
            manager.performAutoTrade(data['strategy'])
        elif action == 'relist':
            manager.relistExpired()
        elif action == 'send-to-club':
            manager.sendWatchlistToClub()
        else:
            return jsonify('What are you doing here, puppy?')

        return jsonify(data)

    def store(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
