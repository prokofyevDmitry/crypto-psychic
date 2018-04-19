import pandas as pd
# from pymongo import MongoClient
# from pymongo.errors import ConnectionFailure
import pprint
import matplotlib.pyplot as plt
from talib.abstract import *
import numpy as np
from constants import *

from stockstats import  StockDataFrame


class DataAnalyzer:
    """
    """

    def __init__(self):
        """
        Establish connection with the database
        If an error is encountred, False is returned.
        """

    # database connection
    # try:
    # 	client = MongoClient('mongodb+srv://dmitryprokofyev:3619738Dd@cluster0-fvwet.mongodb.net/test')
    # 	self.db = client['crypto-psychic']
    # except ConnectionFailure:
    # 	print "Cannot connect to mongoBD"
    # 	return False

    def stockstat(self,dataset):
    	stock = StockDataFrame.retype(dataset)

    	print stock.get('cci_20').tail()

    def william_percent_range(self,dataset,timeperiod):
    	# compute the william renge on timeperiod
    	dataset = dataset[-timeperiod:]
    	return (dataset['high'].max()-dataset.iloc[-1]['close'])/(dataset['high'].max()-dataset['low'].min()) * -100

    def awsome_oscillator(self, dataset):
        """
        awsome oscillator calculation for dataset
        """

        high_sum_low = dataset['high'] + dataset['low']
        high_sum_low = high_sum_low.divide(2)

        high_sum_low = pd.DataFrame(high_sum_low, columns=['close'])

        first = SMA(high_sum_low, timeperiod=5)
        second = SMA(high_sum_low, timeperiod=34)
        return first - second

    def bull_bear_power(self, dataset):
        return dataset['low'] - EMA(dataset, timeperiod=13)

    def buy_pressure(self, dataset):

        # panda serie construction of minimum : current close or previous close
        min = []

        for index, row in dataset.iterrows():
            if index > 0:
                if row['low'] < dataset.iloc[index - 1]['close']:
                    min.append(row['low'])
                else:
                    min.append(dataset.iloc[index - 1]['close'])
            else:
                min.append(row['low'])

        minimums = pd.Series(min)

        return dataset['close'] - minimums

    def ultimate_oscillator(self, dataset):

        TR = TRANGE(dataset)
        BP = self.buy_pressure(dataset)

        average7 = (BP[-7:].sum()) / (TR[-7:].sum())
        average14 = (BP[-14:].sum()) / (TR[-14:].sum())
        average28 = (BP[-28:].sum()) / (TR[-28:].sum())

        return 100 * ((4 * average7) + (2 * average14) + average28) / 7

    # def stoch_rsi(self, dataset):
    #
    #     # results = []
    #
    #     # for index, row in dataset.iterrows():
    #
    #     # 	if index>=26:
    #
    #     # 		rsi = RSI(dataset[:index],timeperiod=14)
    #     # 		print rsi
    #     # 		up = rsi-rsi.min()
    #     # 		down = rsi.max() - rsi.min()
    #     # 		res = ( up.iloc[-1] )/( down ) * 100
    #
    #     # 		results.append( res )
    #
    #     # return pd.Series(results)
    #
    #     return STOCHF(rsi, 14, 3, 3)

    # todo : complete this function !

    def full_analyse(self, index, dataset):

    	stock = StockDataFrame.retype(dataset)

    	results = {}

        results['sma'] = SMA(dataset, timeperiod=EMACROSS_FAST).iloc[-1]

        results['rsi'] = RSI(dataset, timeperiod=RSI_TP).iloc[-1]

        results['cci'] = CCI(dataset, timeperiod=CCI_TP).iloc[-1]

        results['adx'] = ADX(dataset, timeperiod=ADX_TP).iloc[-1]

        results['ao'] = self.awsome_oscillator(dataset).iloc[-1]

        results['mom'] = MOM(dataset, timeperiod=MOM_TP).iloc[-1]

        results['stochf'] = STOCHF(dataset, fastk_period=14, fastd_period=3, fastd_matype=0).iloc[-1]['fastk']

        results['macd'] = stock.get('macd').tail(1)

        results['tochrsi'] = STOCHRSI(dataset, timeperiod=14, fastk_period=14, fastd_period=3, fastd_matype=0).iloc[-1]['fastk']

        results['william_percent_range'] = self.william_percent_range(dataset,timeperiod=WPR_TP)

        results['bul_bea_pwr'] = self.bull_bear_power(dataset).iloc[-1]

        results['uo'] = self.ultimate_oscillator(dataset)

        pprint.pprint(results)



        #sma ema
        timeperiods = [10,20,30,50,100,200]

        sma_ema = {}

        for time in timeperiods:
            name = "SMA {}".format(time)
            sma_ema[name] = SMA(dataset,time).iloc[-1]
            name = "EMA {}".format(time)
            sma_ema[name] = EMA(dataset,time).iloc[-1]


    def emacross(self, index, dataset, historical=HISTORICAL):
        """
        create buy points for
        """
        emaf = SMA(dataset, timeperiod=EMACROSS_FAST)
        emas = SMA(dataset, timeperiod=EMACROSS_SLOW)

        idx = np.argwhere(np.diff(np.sign(emaf - emas)) != 0).reshape(-1) + 0

        idx2 = np.argwhere(np.diff(np.sign(emaf - emas)) > 0).reshape(-1) + 0

        idx3 = np.argwhere(np.diff(np.sign(emaf - emas)) < 0).reshape(-1) + 0

        intesectemafsup = np.intersect1d(idx, idx2)
        intesectemassup = np.intersect1d(idx, idx3)

        ax = dataset['close'].plot()

        emaf.plot(ax=ax)
        emas.plot(ax=ax)

        plt.plot(emaf[intesectemafsup], 'go')
        plt.plot(emaf[intesectemassup], 'ro')

        advice = pd.DataFrame(columns=['SYM', 'TIME', 'PRICE', 'ACTION'])
        # TODO : implement quantity

        if historical is False:
            # we check if the last point is an emacrossing
            if dataset.tail(1).index.item() < intesectemafsup[-1] + 10:
                print "fast up"
                # save buy point
                advice.append(
                    {'SYM': index, 'TIME': dataset.tail()['time'], 'PRICE': dataset.tail()['close'], 'ACTION': -1},
                    ignore_index=True)

                plt.show()

            if dataset.tail(1).index.item() < intesectemassup[-1] + 10 and len(advice.index) > 0:
                advice.append(
                    {'SYM': index, 'TIME': dataset.tail()['time'], 'PRICE': dataset.tail()['close'], 'ACTION': 1},
                    ignore_index=True)


        else:
            # we save all possible advice
            for intersect in intesectemafsup:
                advice = advice.append(
                    {'SYM': index, 'TIME': dataset.ix[intersect]['time'], 'PRICE': dataset.ix[intersect]['close'],
                     'ACTION': -1}, ignore_index=True)
            for intersect in intesectemassup:
                if len(advice.index) > 0:
                    advice = advice.append(
                        {'SYM': index, 'TIME': dataset.ix[intersect]['time'], 'PRICE': dataset.ix[intersect]['close'],
                         'ACTION': 1}, ignore_index=True)

        advice = advice.sort_values('TIME')
        plt.show()
        plt.clf()
        return advice
        self.analyse_advice(index, advice)

    def analyse_advice(self, index, advice):
        """
        prints a clear analysis of all advice for a indexe
        return the gain in %
        """
        # check that there is no advice running:

        values = advice.PRICE * advice.ACTION

        running_advice = advice['ACTION'].sum()
        if running_advice != 1:
            # the last trade is running
            values = values - advice.tail()['PRICE'] * advice.tail()['ACTION']
        value = values.sum()
        print advice
        print "The total gain for {} is {} usd".format(index, value)
        return value

    def analyse(self, index, dataset):
        """
        Calculate all indicators for the dataset and saves them.
        """
        rsi = RSI(dataset, timeperiod=14)

        sma = SMA(dataset, timeperiod=20)

        stochf = STOCHF(dataset, 14, 3, 1)

        print stochf

    def store_analysis(self, result):
        collection = db['analysis']


if __name__ == '__main__':
    dt = DataAnalyzer()
