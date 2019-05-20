import fut
import marketLog
import Sale

class Sell:

	EA_AFTER_TAX_PERCENTAGE = 0.95

	def __init__(self):
        self.pricing = new Pricing();

	def calculateSellPrice(self, Item):

		derivative = self.pricing.getDerivative(Item.itemId)
		currentPrice = derivative.current
		futurePrice = derivative.future
		tendency = derivative.tendency

		sellPrice = currentPrice

		if tendency.increasing:
			sellPrice = futurePrice
		elif tendency.decreasing:
			sellPrice = currentPrice

		profitOrLoss = (sellPrice * self.EA_AFTER_TAX_PERCENTAGE - Item.buyingPrice)

		if profitOrLoss < 0:
			return None

		return sellPrice


	def sell(self, Item):

		sellPrice = self.calculateSellPrice(Item)

		if sellPrice == None:
			return

		session = fut.Core('email', 'password', platform='ps4')
		session.sell(Item.itemId, sellPrice, buy_now = sellPrice + 900, duration = 3600)
		# marketLog.log(new Sale(Item.itemId, sellPrice, buy_now, duration)) use queue
