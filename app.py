import fut
import numpy as np
import csv
import pandas as pd
from fbprophet import Prophet
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from src.modules.scrapers.futbinScraper import FutbinImporter

f = FutbinImporter()
data = f.getPlayerPriceHistory(155862, 'daily_graph')
# data = data + f.getPlayerPriceHistory(155862, 'da_yesterday')
# data = data + f.getPlayerPriceHistory(155862, 'today')
a = np.asarray(data)
csv = open('./data/single-player.csv', "w")
csv.write("ds,"+ "y"+"\n")

for v in data:
	row = str(datetime.fromtimestamp(v['time']).strftime('%Y-%M-%d')) + "," + str(v['price']) + "\n"
	csv.write(row)
csv.close()

df = pd.read_csv('./data/single-player.csv')
df.head()
m = Prophet(changepoint_prior_scale=0.01)
m.fit(df)
m.plot(df)
future = m.make_future_dataframe(periods=365)
future.tail()
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
forecast.plot()


