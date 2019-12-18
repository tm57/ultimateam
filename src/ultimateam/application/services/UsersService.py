from src.ultimateam.repositories.users.mongoDB.UsersRepository import UsersRepository


class UsersService:
    def __init__(self):
        self._users_repository = UsersRepository()

    def createUser(self, email, password, passphrase):
        data = {
            'email': email,
            'password': password,
            'passphrase': passphrase
        }
        return self._users_repository.create(data)

    def getUsers(self, limit=10):
        return self._users_repository.getUsers(limit=limit)

    def getUser(self, user_id):
        return self._users_repository.getUser(user_id)
