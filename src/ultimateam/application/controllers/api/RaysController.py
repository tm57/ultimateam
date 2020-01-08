from bson.json_util import dumps

from src.ultimateam.application.services.RaysService import RaysService


class RaysController:
    def __init__(self, request):
        self.service = RaysService()
        self.request = request

    def index(self):
        return self.service.getActiveRays()

    def store(self):
        form = self.request.form
        ray_id = form['ray_id']
        strategy = form['strategy']
        status = form['status']
        return dumps(self.service.createRay(ray_id, strategy, status))

    def delete(self):
        ray_id = self.request.form['ray_id']
        return self.service.deleteRay(ray_id)

    def update(self):
        pass
