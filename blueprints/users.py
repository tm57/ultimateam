from flask import Blueprint, request

from src.ultimateam.application.controllers.api.UsersController import UsersController

users = Blueprint('users', __name__)


@users.route("/users", methods=["POST"])
def createUser():
    ctrl = UsersController()
    user_info = request.form

    return ctrl.createUser(user_info)


@users.route("/users", methods=["GET"])
def getUsers():
    ctrl = UsersController()
    return ctrl.getUsers()
