from flask import Flask, jsonify
import os

from blueprints.users import users
from blueprints.rays import rays
from blueprints.trading import trading


from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(rays)
app.register_blueprint(trading)
app.register_blueprint(users)


@app.route("/", methods=["GET"])
def index():
    return jsonify('It works')


if __name__ == "__main__":
    env = os.environ.get('APP_ENV', 'development')
    port = int(os.environ.get('APP_PORT'))
    debug = env == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
