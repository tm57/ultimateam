from src.modules.fut.constants import PILE_SIZE


class ClubFetcher:
    def __init__(self, client, fetcher):
        self.client = client
        self.fetcher = fetcher

    def fetch(self):
        client = self.client
        available_slots = PILE_SIZE - len(client.tradepile())
        items = self.fetcher.fetch()
        return items[0:available_slots]
