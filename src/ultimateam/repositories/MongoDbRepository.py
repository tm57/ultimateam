from src.ultimateam.repositories.drivers.mongoDriver import MongoDriver


class MongoDbRepository:
    def __init__(self):
        self.client = MongoDriver().getClient()
