import requests
from datetime import datetime

class FutbinImporter:
  TODAY = "today"
  YESTERDAY = "yesterday"
  DAY_BEFORE_YESTERDAY = "da_yesterday"

  def getPlayerPriceHistory(self, id, period):
    r = requests.get('https://www.futbin.com/19/playerGraph?type='+period+'&year=19&player={0}'.format(id))
    data = r.json()
    result = [];
    # We are only doing for PS for now
    for price in data['ps']:
      
      result.append({"time": price[0]/ 1000 , "price": price[1]})
    return result;
