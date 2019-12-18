import jsonschema
from flask import Blueprint, request, Response
from flask_jsonschema_validator import JSONSchemaValidator

from src.ultimateam.application.controllers.api.ExchangeController import ExchangeController

exchange = Blueprint('exchange', __name__)
JSONSchemaValidator(app=exchange, root="schemas")


@exchange.route('/handshake', methods=['POST'])
@exchange.validate('exchange', 'fut_info')
def handshake():
    # request for permission to exchange
    # if we are happy we give you a token to trade else we say bye
    ctrl = ExchangeController(request)
    return ctrl.handshake()


@exchange.route('/exchange', methods=['POST'])
def exchange():
    # initiate the exchange, i.e start distribution of the requested resources
    ctrl = ExchangeController(request)
    return ctrl.performExchange()


@exchange.route('/rays', methods=['POST'])
def delete():
    ctrl = ExchangeController(request)
    return ctrl.delete()


@exchange.errorhandler(jsonschema.ValidationError)
def onValidationError(e):
    return Response("There was a validation error: " + str(e), 400)
