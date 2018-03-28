from datagrabber.datagrabber import DataGrabber
from dataanalyzer.dataanalyzer import DataAnalyzer 
import csv



# uses close prices (default)
 



with open('crypto_list.csv', mode='r') as crypto_list_csv:
	reader = csv.reader(crypto_list_csv)
	crypto_list = []
	for rows in reader:
		crypto_list.append(rows[0])



dtgrab = DataGrabber("hour")
dtanalyser = DataAnalyzer()


result = 0

crypto_list = ['NEO']

for crypto in crypto_list:

	df_data = dtgrab.grab(crypto)

	#result+=dtanalyser.analyse_advice(crypto,dtanalyser.emacross(crypto,df_data))
	dtanalyser.full_analyse(crypto,df_data)

print "Total result: {}".format(result)	








	



