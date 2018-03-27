from datagrabber.datagrabber import DataGrabber
from dataanalyzer.dataanalyzer import DataAnalyzer 
import csv



# uses close prices (default)
 



with open('crypto_list.csv', mode='r') as crypto_list_csv:
	reader = csv.reader(crypto_list_csv)
	crypto_list = []
	for rows in reader:
		crypto_list.append(rows[0])



dtgrab = DataGrabber("day")
dtanalyser = DataAnalyzer()


result = 0

for crypto in crypto_list:

	df_data = dtgrab.grab(crypto)

	result+=dtanalyser.analyse_trades(crypto,dtanalyser.emacross(crypto,df_data))

print "Total result: {}".format(result)	








	



