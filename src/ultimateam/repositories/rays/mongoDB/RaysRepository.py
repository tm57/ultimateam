from interface import implements

from src.ultimateam.repositories.MongoDbRepository import MongoDbRepository
from src.ultimateam.repositories.rays.RaysRepositoryInterface import RaysRepositoryInterface


class RaysRepository(implements(RaysRepositoryInterface), MongoDbRepository):

    def create(self, ray_id, strategy, status):

        data = {
            'ray_id': ray_id,
            'strategy': strategy,
            'status': status
        }
        return self.client.db.rays.insert(data)

    def getActiveRays(self):
        return self.client.db.rays.find({'status': 1})

    def delete(self, ray_id):
        return self.client.db.rays.delete({'ray_id': ray_id})
