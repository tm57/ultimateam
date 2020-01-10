from flask import Blueprint, request

from src.ultimateam.application.controllers.api.TradingController import TradingController

trading = Blueprint('trading', __name__)


@trading.route('/run', methods=['POST'])
def run():

    ctrl = TradingController(request)
    return ctrl.run()
