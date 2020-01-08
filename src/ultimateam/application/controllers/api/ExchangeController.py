from flask import jsonify

from src.ultimateam.application.services.ExchangeService import ExchangeService


class ExchangeController:
    def __init__(self, request):
        self.service = ExchangeService()
        self.request = request

    def index(self):
        pass

    async def performExchange(self):
        request = self.request
        exchange_token = request.form['token']
        await self.service.performExchange(exchange_token)
        return jsonify('Exchange initiated')

    def delete(self):
        pass

    def update(self):
        pass

    def handshake(self):
        request = self.request
        fut_info = request.form['user']['fut']
        domain_user = request.form['user']['domain']  # we should get this from auth
