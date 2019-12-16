from interface import implements

from src.ultimateam.repositories.MongoDbRepository import MongoDbRepository
from src.ultimateam.repositories.users.UsersRepositoryInterface import UsersRepositoryInterface


class UsersRepository(implements(UsersRepositoryInterface), MongoDbRepository):

    def create(self, email, password, passphrase):
        data = {
            'email': email,
            'password': password,
            'passphrase': passphrase
        }
        return self.client.db.users.insert(data)

    def getUsers(self, **kwargs):
        return self.client.db.users.find().limit(kwargs['limit'])

    def getUser(self, user_id):
        return self.client.db.users.find({'user_id': user_id}).limit(1)
