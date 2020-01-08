from src.ultimateam.repositories.rays.mongoDB.RaysRepository import RaysRepository


class RaysService:

    def __init__(self):
        self._rays_repository = RaysRepository()

    def createRay(self, ray_id, strategy, status):
        data = {
            'ray_id': ray_id,
            'strategy': strategy,
            'status': status
        }
        return self._rays_repository.create(data)

    def getActiveRays(self):
        return self._rays_repository.getActiveRays()

    def deleteRay(self, ray_id):
        return self._rays_repository.delete({'ray_id': ray_id})

    def getTraderRay(self, target_credit: int):
        criteria = {
            'credit': {'gt': target_credit},
            'status': 0,
            'buy_ray': None
        }
        return self._rays_repository.find(criteria)
