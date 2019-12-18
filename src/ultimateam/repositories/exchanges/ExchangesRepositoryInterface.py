from interface import Interface


class ExchangesRepositoryInterface(Interface):
    def __init__(self):
        pass

    def find(self, criteria: dict):
        pass
