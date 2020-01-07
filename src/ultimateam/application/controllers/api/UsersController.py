from flask import jsonify

from src.ultimateam.application.services.UsersService import UsersService

from bson.json_util import dumps


class UsersController:
    def __init__(self):
        self.user_service = UsersService()
        pass

    def createUser(self, user_info):
        if user_info is None:
            return jsonify({'error': u'Error Invalid User Info provided'})

        email = user_info['email']
        password = user_info['password']
        passphrase = user_info['passphrase']
        user_id = self.user_service.createUser(email, password, passphrase)
        resp = jsonify({'id': str(user_id)})

        resp.headers['RAY-ID'] = str(user_id)
        return resp

    def getUsers(self):
        return dumps(self.user_service.getUsers())
