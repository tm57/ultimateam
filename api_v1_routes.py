import asyncio
import json

from flask import Flask, request, jsonify
import os

from blueprints.rays import rays
from src.ultimateam.TransferMarketManager import TransferMarketManager
from src.ultimateam.application.controllers.api.UsersController import UsersController

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(rays)


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    # email = data['email']
    # password = data['password']
    # passphrase = data['passphrase']
    # print email, passphrase, password

    return jsonify(request.get_json())


@app.route("/relist", methods=["POST"])
def relist():
    # response = manager.relistExpired()
    # return jsonify(response)
    pass


@app.route("/auto", methods=["POST"])
def auto():
    futures = []
    with open('seeds/users.json') as json_file:
        ray_mastereo = json.load(json_file)

        for ray in ray_mastereo:
            manager = TransferMarketManager(ray['email'], ray['password'], ray['passphrase'])
            futures.append({'manager': manager, 'strategy': ray['strategy']})
        print('Starting async selling')

    asyncio.run(main(futures))
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


async def main(callables):
    return await asyncio.gather(*((data['manager'].performAutoTrade('sniper')) for data in callables))


if __name__ == "__main__":
    env = os.environ.get('APP_ENV', 'development')
    port = int(os.environ.get('APP_PORT', 3000))
    debug = False if env == 'production' else True
    app.run(host='0.0.0.0', port=port, debug=debug)
