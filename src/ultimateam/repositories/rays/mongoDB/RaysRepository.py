from interface import implements

from src.ultimateam.repositories.MongoDbRepository import MongoDbRepository
from src.ultimateam.repositories.rays.RaysRepositoryInterface import RaysRepositoryInterface


class RaysRepository(implements(RaysRepositoryInterface), MongoDbRepository):
    collection = 'rays'

    def getActiveRays(self):
        return super().find({'status': 1})
