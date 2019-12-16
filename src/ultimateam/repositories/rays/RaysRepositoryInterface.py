from interface import Interface


class RaysRepositoryInterface(Interface):
    def create(self, ray_id, strategy, status):
        pass

    def delete(self, ray_id):
        pass

    def getActiveRays(self):
        pass
