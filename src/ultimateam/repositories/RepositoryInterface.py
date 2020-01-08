from interface import Interface


class RepositoryInterface(Interface):
    def find(self, criteria: dict):
        pass

    def delete(self, criteria: dict):
        pass

    def create(self, criteria: dict):
        pass
