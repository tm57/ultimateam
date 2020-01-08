from interface import implements

from src.ultimateam.repositories.MongoDbRepository import MongoDbRepository
from src.ultimateam.repositories.users.UsersRepositoryInterface import UsersRepositoryInterface


class UsersRepository(implements(UsersRepositoryInterface), MongoDbRepository):
    collection = 'users'

    def getUsers(self, **kwargs):
        return super().find({}).limit(kwargs['limit'])

    def getUser(self, user_id):
        return super().find({'user_id': user_id}).limit(1)
