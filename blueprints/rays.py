from flask import Blueprint, request

from src.ultimateam.application.controllers.api.RaysController import RaysController

rays = Blueprint('rays', __name__)


@rays.route('/rays', methods=['GET'])
def getRays():
    ctrl = RaysController(request)
    return ctrl.index()


@rays.route('/rays', methods=['POST'])
def store():
    ctrl = RaysController(request)
    return ctrl.store()


@rays.route('/rays', methods=['POST'])
def delete():
    ctrl = RaysController(request)
    return ctrl.delete()
