from src.ultimateam.repositories.rays.mongoDB.RaysRepository import RaysRepository


class RaysService:
    def __init__(self):
        self._rays_repository = RaysRepository()

    def createRay(self, ray_id, strategy, status):
        return self._rays_repository.create(ray_id, strategy, status)

    def getActiveRays(self):
        return self._rays_repository.getActiveRays()

    def deleteRay(self, ray_id):
        return self._rays_repository.delete(ray_id)
