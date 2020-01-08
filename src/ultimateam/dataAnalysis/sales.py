from datetime import datetime, date, time, timedelta

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import pandas as pd


class Sales:
    def __init__(self):
        pass

    @staticmethod
    def aggregates():
        f = "./data/sell-log.csv"

        df = pd.read_csv(f,
                         header=None,
                         converters={'timestamp': lambda x: datetime.utcfromtimestamp(float(x))},
                         names=['timestamp', 'count', 'price']
                         )\
            .drop(columns=['count'])

        df = df.set_index('timestamp')
        df1 = df.groupby(by=[df.index.date]).sum()
        df1.plot.bar()
        plt.show(block=True)

    @staticmethod
    def plotLine():
        DataAll1D = np.loadtxt("./data/sell-log.csv", delimiter=",")

        time = list(DataAll1D[:, 0])
        coin = list(DataAll1D[:, 2])
        plt.plot(time, coin)
        plt.xticks(time, coin)
        plt.ylabel('Coin')
        plt.title('Sales with time')

        plt.show()

    @staticmethod
    def plotBar():
        data = np.loadtxt("./data/sell-log.csv", delimiter=",")
        days = list(map(lambda x: datetime.utcfromtimestamp(x), data[:, 0]))
        amounts = list(data[:, 2])
        combined = zip(days, amounts)

        start = days[0]
        end = days[len(days) - 1]
        date_generated = [start + timedelta(days=x) for x in range(0, (end.day - start.day))]
        points = []

        for dt in date_generated:
            x = {
                'amount': 0,
                'date': dt
            }

            points.append(x)

        for p in points:
            for item in combined:
                observed_day, amount = item
                if p['date'].day == observed_day.day:
                    p['amount'] += amount

        x = map(lambda ptr: ptr['date'], points)

        y = map(lambda ptr: ptr['amount'], points)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        plt.bar(x, y, width=.7, align='edge')
        plt.title("Sales", fontsize=22)
        plt.ylabel('# coins')
        plt.show()


if __name__ == '__main__':
    g = Sales()
    g.aggregates()
