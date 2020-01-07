from interface import implements

from src.ultimateam.repositories.RepositoryInterface import RepositoryInterface
from src.ultimateam.repositories.drivers.mongoDriver import MongoDriver


class MongoDbCollectionMissingException(Exception):
    pass


class MongoDbRepository(implements(RepositoryInterface)):
    collection = ''

    def __init__(self):
        if self.collection == '':
            raise MongoDbCollectionMissingException()
        self.client = MongoDriver().getClient()
        self.model = self.client.db[self.collection]

    def find(self, criteria: dict):
        return self.model.find(criteria)

    def delete(self, criteria: dict):
        return self.model.delete(criteria)

    def create(self, criteria: dict):
        return self.model.insert(criteria)
