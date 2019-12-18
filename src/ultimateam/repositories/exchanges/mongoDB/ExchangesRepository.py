from interface import implements

from src.ultimateam.repositories.MongoDbRepository import MongoDbRepository
from src.ultimateam.repositories.exchanges.ExchangesRepositoryInterface import ExchangesRepositoryInterface


class ExchangesRepository(MongoDbRepository, implements(ExchangesRepositoryInterface)):
    collection = 'exchanges'



