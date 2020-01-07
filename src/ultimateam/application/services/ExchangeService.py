from src.ultimateam.TransferMarketManager import TransferMarketManager
from src.ultimateam.application.services.RaysService import RaysService
from src.ultimateam.fut.constants import EA_TAX_PERCENTAGE, EXCHANGE_STRATEGY
from src.ultimateam.repositories.exchanges.mongoDB.ExchangesRepository import ExchangesRepository
from src.ultimateam.repositories.rays.mongoDB.RaysRepository import RaysRepository


class CreditTooLowException(Exception):
    pass


class ExchangeService:
    ALLOWANCE_CREDIT = 10000
    TEN_K = 10000
    SELLER_RAY = 1
    MAX_PRICE = 400

    def __init__(self):
        self._exchanges_repository = ExchangesRepository()
        self._rays_repository = RaysRepository()
        self._rays_service = RaysService()

    async def performExchange(self, exchange_token):
        trade_info = self._exchanges_repository.find({'token': exchange_token})

        if trade_info is None:
            return False

        buy_ray = trade_info.buy_ray
        buyer = TransferMarketManager(*buy_ray)
        buy_criteria = self.getBuyCriteria(trade_info.target)
        await buyer.performBuy(strategy_name=EXCHANGE_STRATEGY, **buy_criteria)
        trade_ids = await buyer.performSell(EXCHANGE_STRATEGY)

        buy_criteria = self.getBuyCriteria(trade_info.target, ray_type=self.SELLER_RAY)
        min_credit_from_seller = buy_criteria['quantity'] * buy_criteria['price'] + self.ALLOWANCE_CREDIT
        seller_ray = self._rays_service.getTraderRay(min_credit_from_seller)
        seller = TransferMarketManager(*seller_ray)
        return seller.performBuy(strategy_name=EXCHANGE_STRATEGY, **buy_criteria, trade_ids=trade_ids)

    def _getBuyQuantity(self, target_value: int) -> int:

        if target_value <= self.TEN_K:
            return 1

        temp_quantity = int(target_value / self.TEN_K)
        remaining_value = target_value * (1 - EA_TAX_PERCENTAGE)
        return temp_quantity + self._getBuyQuantity(remaining_value)

    def getBuyCriteria(self, target_credit: int, ray_type=0) -> dict:
        quantity = self._getBuyQuantity(target_credit)

        criteria = {
            'quantity': quantity,
            'type': 'player',
            'level': 'gold',
            'max_buy': 1000,
            'max_price': self.MAX_PRICE
        }

        if ray_type == self.SELLER_RAY:
            excess = int(quantity * self.TEN_K - target_credit)
            criteria['excess_value'] = excess
            criteria['max_buy'] = self.TEN_K
            criteria['max_price'] = None

        return criteria
