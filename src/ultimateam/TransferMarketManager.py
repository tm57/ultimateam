import random

from src.ultimateam.clubItemFetchers.ClubFetcher import ClubFetcher
from src.ultimateam.clubItemFetchers.Gold300ClubFetcher import Gold300ClubFetcher
from src.ultimateam.clubItemFetchers.SFclubFetcher import SFclubFetcher
from src.ultimateam.fut.buyStrategies.exchanger import Exchanger
from src.ultimateam.fut.exceptions.InvalidClubFetcherException import InvalidClubFetcherException
from src.ultimateam.fut.sellerStrategies.exchangeSeller import ExchangeSeller
from src.ultimateam.fut.sellerStrategies.sellerPolicies.exchangeSellerPolicy import ExchangeSellerPolicy
from src.ultimateam.fut.sellerStrategies.sellerPolicies.sniperSellerPolicy import SniperSellerPolicy
from src.utils.utils import sendMessage, log, sleep
from src.ultimateam.fut.buyStrategies.gold300buyer import Gold300Buyer
from src.ultimateam.fut.buyStrategies.sniper import Sniper
from src.ultimateam.fut.buyer import Buyer
from src.ultimateam.fut.exceptions.InvalidBuyStrategyException import InvalidBuyStrategyException
from src.ultimateam.fut.exceptions.InvalidSellStrategyException import InvalidSellStrategyException
from src.ultimateam.fut.futClient import FutClient
from src.ultimateam.fut.seller import Seller
from src.ultimateam.fut.sellerStrategies.gold300Seller import Gold300Seller
from src.ultimateam.fut.sellerStrategies.sniperSeller import SniperSeller
from src.ultimateam.fut.constants import *


class TransferMarketManager:
    AUTO_TRADE_PILE_SIZE_LIMIT = 95

    def __init__(self, email, password, passphrase):
        self.item_ids = []
        fut = FutClient(email, password, passphrase)
        self.bot_name = passphrase
        self.client = fut.getClient()

    async def performTradePileCleanup(self):
        num_sold = self.sold()

        if num_sold > 0:
            self.client.tradepileClear()

        self.relistExpired()

    def cleanUpWatchlistOutBid(self):

        items = self.client.watchlist()
        for item in items:
            trade_id = item['tradeId']
            trade_state = item['tradeState']
            bid_state = item['bidState']
            if trade_state == TRADE_STATUS_CLOSED and bid_state == BID_STATE_OUTBID:
                self.client.watchlistDelete(trade_id)
                print('--> Removed item with trade id: %d because we are outbid ' % trade_id)

    def moveItemsToTradePile(self, strategy):

        watch_list_items = self.client.watchlist()

        won_items = list(filter(
            lambda x: x['tradeState'] == TRADE_STATUS_CLOSED and x['bidState'] == BID_STATE_HIGHEST,
            watch_list_items
        ))
        unassigned = self.client.unassigned()
        item_ids = map(lambda x: x['id'], won_items + unassigned)

        num_slots = PILE_SIZE - len(self.client.tradepile())
        num_moved = 0
        for item_id in item_ids:
            if num_slots >= 1:
                self.client.sendToTradepile(item_id, safe=False)
                num_slots -= 1
                num_moved += 1

        print('-->  %d items have been moved from watchlist/unassigned to trade pile' % num_moved)
        self.fetchItemsFromClubToTradepile(strategy)

    async def performSell(self, strategy_name):
        await self.performTradePileCleanup()
        self.moveItemsToTradePile(strategy_name)
        rule = None

        if strategy_name not in [SELL_STRATEGY_SNIPER, SELL_STRATEGY_G300, EXCHANGE_STRATEGY]:
            raise InvalidSellStrategyException(strategy_name)

        if strategy_name == SELL_STRATEGY_SNIPER:
            rule = SniperSellerPolicy(1200, 1500)

        if strategy_name == EXCHANGE_STRATEGY:
            rule = ExchangeSellerPolicy().get()

        strategy = self.getSellerStrategy(strategy_name, rule=rule)

        seller = Seller(strategy, self.client)
        tradepile = self.client.tradepile()
        items = filter(lambda x: x['tradeState'] is None, tradepile)

        item_ids = map(lambda x: x['id'], items)
        return await seller.sell(item_ids=item_ids)

    async def performBuy(self, strategy_name, send_to_club=False, **kwargs):
        self.cleanUpWatchlistOutBid()
        strategy = self.getBuyStrategy(strategy_name, **kwargs)
        buyer = Buyer(strategy)
        await buyer.buy()

        if send_to_club:
            self.sendWatchlistToClub()

    async def performAutoTrade(self, strategy_name):
        ok = True
        initial_balance = self.client.keepalive()

        while ok:
            await self.performBuy(strategy_name)
            await self.performSell(strategy_name)
            balance = self.client.keepalive()
            pile_size = self.pileSize()
            if pile_size >= self.AUTO_TRADE_PILE_SIZE_LIMIT:
                msg = self.bot_name + 'Auto trade is stopping now' \
                                      '\n-->INITIAL BALANCE: %d\n' \
                                      '--> NEW BALANCE: %d' \
                                      '\nPROFIT/LOSS %d\n' \
                                      'Tradepile Size: %d' % (
                          initial_balance, balance, (balance - initial_balance), pile_size)
                print(msg)
                sendMessage(msg)
                break

    def pileSize(self):
        return len(self.client.tradepile())

    def getBuyStrategy(self, name, **kwargs):
        if name == GOLD300_STRATEGY:
            return Gold300Buyer(self.client)
        if name == SNIPER_STRATEGY:
            return Sniper(self.client)
        if name == EXCHANGE_STRATEGY:
            return Exchanger(self.client, **kwargs)
        raise InvalidBuyStrategyException(name + 'is an invalid buy strategy')

    def getSellerStrategy(self, name, rule=None):
        if name == GOLD300_STRATEGY:
            return Gold300Seller(self.client)
        if name == SNIPER_STRATEGY:
            return SniperSeller(self.client, rule)
        if name == EXCHANGE_STRATEGY:
            return ExchangeSeller(self.client, rule)
        raise InvalidSellStrategyException(name + 'is an invalid sell strategy')

    def sold(self):
        tradepile = self.client.tradepile()
        sold = 0
        bids = 0
        for i in range(0, len(tradepile)):
            if tradepile[i]['tradeState'] == TRADE_STATUS_CLOSED:
                sold += 1
                bids += tradepile[i]['currentBid']

        if bids == 0:
            msg = 'Nothing sold at this point'
            print(msg)
            sendMessage(msg)
            return 0
        revenue = int(bids * EA_TAX_PERCENTAGE)
        msg = 'Sold %s items for %s coins' % (sold, revenue)
        csv = str(sold) + ',' + str(revenue) + '\n'
        sendMessage(msg)
        log(csv)
        return sold

    def sendWatchlistToClub(self):
        items = self.client.watchlist()
        num_sent = 0
        for item in items:
            item_id = item['id']

            status = self.client.sendToClub(item_id)
            num_sent = num_sent + 1 if status else num_sent
            time_to_sleep = random.randint(0, 3)
            sleep(time_to_sleep)
        msg = 'Sent %d items to club' % num_sent
        print(msg)
        sendMessage(msg)

    def relistExpired(self):
        pile = self.client.tradepile()
        num_expired = len(list(filter(lambda x: x['tradeState'] == TRADE_STATE_EXPIRED, pile)))

        if num_expired > 0:
            self.client.relist()

        msg = 'Relisted %d items' % num_expired
        print(msg)
        sendMessage(msg)

    def fetchItemsFromClubToTradepile(self, strategy):
        fetcher = None
        if strategy == GOLD300_STRATEGY:
            fetcher = Gold300ClubFetcher(self.client)
        elif strategy == SNIPER_STRATEGY:
            fetcher = SFclubFetcher(self.client)

        if fetcher is None:
            raise InvalidClubFetcherException('A strategy needs to be provided so we know how to fetch from club')

        club_fetcher = ClubFetcher(self.client, fetcher)
        item_ids = club_fetcher.fetch()

        if not item_ids:
            print('Nothing moved from club')
            return

        for item_id in item_ids:
            self.client.sendToTradepile(item_id, safe=False)
            time_to_sleep = random.randint(0, 3)
            sleep(time_to_sleep)
        msg = 'Moved %d items from club to tradepile' % len(item_ids)
        print(msg)
        sendMessage(msg)
