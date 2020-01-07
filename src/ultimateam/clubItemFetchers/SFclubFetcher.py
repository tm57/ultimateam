from src.ultimateam.fut.constants import DEF_ID_SQUAD_FITNESS


class SFclubFetcher:

    def __init__(self, client):
        self.client = client

    @staticmethod
    def getCriteria():
        return {
            'ctype': 'development',
            'defId': DEF_ID_SQUAD_FITNESS
        }

    @staticmethod
    def filterItem(item):
        price = item['lastSalePrice']
        item_id = None
        if 0 < price <= 900:
            item_id = item['id']
        return item_id

    def fetch(self):
        return []
