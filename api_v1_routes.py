import json

from flask import Flask, request, jsonify
import os

from blueprints.rays import rays
from blueprints.trading import trading
from src.ultimateam.TransferMarketManager import TransferMarketManager
from src.ultimateam.application.controllers.api.UsersController import UsersController

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(rays)
app.register_blueprint(trading)


@app.route("/relist", methods=["POST"])
def relist():
    # response = manager.relistExpired()
    # return jsonify(response)
    pass


@app.route("/auto", methods=["POST"])
def auto():
    data = request.get_json()
    manager = TransferMarketManager(data['email'], data['password'], data['passphrase'], data['codes'])
    manager.performAutoTrade(data['strategy'])

    return jsonify('Jobs running now, check your messaging up for updates 🤞')


@app.route("/users", methods=["POST"])
def createUser():
    users = UsersController()
    user_info = request.form

    return users.createUser(user_info)


@app.route("/users", methods=["GET"])
def getUsers():
    users = UsersController()
    return users.getUsers()


@app.route("/", methods=["GET"])
def index():
    return jsonify('It works')


if __name__ == "__main__":
    env = os.environ.get('APP_ENV', 'development')
    port = int(os.environ.get('APP_PORT', 3000))
    debug = False if env == 'production' else True
    app.run(host='0.0.0.0', port=port, debug=debug)
