from src.modules.TransferMarketManager import TransferMarketManager
from dotenv import load_dotenv
import argparse

from src.utils.utils import sendMessage

load_dotenv()

manager = TransferMarketManager()

parser = argparse.ArgumentParser()
parser.add_argument("--action", help="Command, buy, sell, send to club", type=str)
parser.add_argument("--strategy", help="Which algorithm to use", type=str)
parser.add_argument("--to_club", help="whether to send bought items to club", type=int)

args = parser.parse_args()
action = args.action
strategy = args.strategy
to_club = args.to_club

try:
    if action == 'buy':
        manager.performBuy(strategy_name=strategy, send_to_club=bool(to_club))
    elif action == 'sell':
        manager.performSell(strategy)
    elif action == 'auto':
        manager.performAutoTrade(strategy)
    elif action == 'send-to-club':
        manager.sendWatchlistToClub()
    elif action == 'relist':
        manager.relistExpired()

except Exception as e:
    sendMessage(
        ':warning:  There was exception, check the app asap :warning: \n' + e.message
    )
