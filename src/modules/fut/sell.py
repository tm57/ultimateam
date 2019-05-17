import fut

class Sell:

	EA_AFTER_TAX_PERCENTAGE = 0.95

	def __init__(self):
        self.pricing = new Pricing();

	def calculateSellPrice(self, Item):

		derivative = self.pricing.getDerivative(Item.item_id)
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

		if(sellPrice)



