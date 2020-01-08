class Gold300ClubFetcher:

    def __init__(self, client):
        self.client = client

    @staticmethod
    def getCriteria():
        return {
            'ctype': 'player',
            'level': 'gold'
        }

    def filterItem(self, item):
        price = item['lastSalePrice']
        item_id = None
        if 0 < price <= 350 or item['marketDataMinPrice'] == 350:
            item_id = item['id']
        return item_id

    def fetch(self):
        return []
        start = 0
        max_to_fetch = 15
        result = []
        ok = True
        num_requests = 5
        request_count = 0
        while ok:
            if request_count >= num_requests:
                break
            items = self.client.club(ctype='player', level='gold', start=start)
            start += len(items)
            request_count += 1

            for item in items:
                item_id = self.filterItem(item)
                if item_id:
                    result.append(item_id)

                if len(result) >= max_to_fetch:
                    break
                if len(items) == 0:
                    break
        return result
