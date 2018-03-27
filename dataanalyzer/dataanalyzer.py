import pandas as pd 
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pprint
import matplotlib.pyplot as plt
from talib.abstract import *
import numpy as np
from constants import *
class DataAnalyzer:
	"""
	"""
	def __init__(self):
		"""
		Establish connection with the database
		If an error is encountred, False is returned. 
		"""

		#database connection
		try:
			client = MongoClient('mongodb+srv://dmitryprokofyev:3619738Dd@cluster0-fvwet.mongodb.net/test')
			self.db = client['crypto-psychic']
		except ConnectionFailure: 
			print "Cannot connect to mongoBD"
			return False


	def emacross(self,index,dataset,historical=HISTORICAL):
		"""
		create buy points for 
		"""
		emaf = SMA(dataset, timeperiod=EMACROSS_FAST)
		emas = SMA(dataset, timeperiod=EMACROSS_SLOW)


		ax = dataset['close'].plot()

		emaf.plot(ax=ax)
		emas.plot(ax=ax)

		idx = np.argwhere(np.diff(np.sign(emaf - emas)) != 0).reshape(-1) + 0
		
		idx2 = np.argwhere(np.diff(np.sign(emaf - emas)) > 0).reshape(-1) + 0
		
		idx3 = np.argwhere(np.diff(np.sign(emaf - emas)) < 0).reshape(-1) + 0

		intesectemafsup = np.intersect1d(idx,idx2)
		intesectemassup = np.intersect1d(idx,idx3)


		plt.plot(emaf[intesectemafsup], 'go')
		plt.plot(emaf[intesectemassup], 'ro')


		trades = pd.DataFrame(columns=['SYM','TIME','PRICE','ACTION'])
		# TODO : implement quantity
		
		if historical is False:
			# we check if the last point is an emacrossing 
			if dataset.tail(1).index.item() < intesectemafsup[-1]:
				print "fast up"
				#save buy point
				trades.append({'SYM':index,'TIME':dataset.tail()['time'],'PRICE':dataset.tail()['close'],'ACTION':-1},ignore_index=True)

				


			if dataset.tail(1).index.item() < intesectemassup[-1]:
				print "fast down"
				if len(trades.index)>0:
					trades.append({'SYM':index,'TIME':dataset.tail()['time'],'PRICE':dataset.tail()['close'],'ACTION':+1},ignore_index=True)

		else:
			#we save all possible trades
			for intersect in intesectemafsup:
				trades=trades.append({'SYM':index,'TIME':dataset.ix[intersect]['time'],'PRICE':dataset.ix[intersect]['close'],'ACTION':-1},ignore_index=True)
			for intersect in intesectemassup:
				if len(trades.index)>0:
					trades=trades.append({'SYM':index,'TIME':dataset.ix[intersect]['time'],'PRICE':dataset.ix[intersect]['close'],'ACTION':1},ignore_index=True)

		trades = trades.sort_values('TIME')
		

		return trades
		self.analyse_trades(index,trades)


	def analyse_trades(self,index,trades):
		"""
		prints a clear analysis of all trades for a indexe
		return the gain in %
		"""
		# check that there is no trades running: 

		values = trades.PRICE * trades.ACTION
		
		running_trade = trades['ACTION'].sum()
		if running_trade != 0:
			# the last trade is running
			values  = values - trades.tail()['PRICE']*trades.tail()['ACTION']
		value = values.sum()
		
		print "The total gain for {} is {} usd".format(index,value)
		return value



	def analyse(self, index, dataset):
		"""
		Calculate all indicators for the dataset and saves them. 
		"""
		rsi = RSI(dataset,timeperiod=14)
		
		sma = SMA(dataset, timeperiod=20)

		

		stochf = STOCHF(dataset,14,3,1)

		

		print stochf

	def store_analysis(self,result):
		collection = db['analysis']




if __name__ == '__main__':
    
    dt = DataAnalyzer()