from interface import implements
from pymongo import MongoClient
import os

from src.ultimateam.repositories.drivers.StorageDriverInterface import StorageDriverInterface


class MongoDriver(implements(StorageDriverInterface)):
    def __init__(self):
        self._client = MongoClient(os.getenv('MONGO_DB_URL', 'localhost'), int(os.getenv('MONGO_DB_PORT', 27017)))

    def getClient(self):
        return self._client
