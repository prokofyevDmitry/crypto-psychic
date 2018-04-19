"""
Datagrabber class responsible for the fetching of historical cryptocurrency stock data.
"""
import datetime

import pandas as pd
import requests


class DataGrabber:
    """

    """

    def __init__(self, period, api_base_path="https://min-api.cryptocompare.com/data/histo", max_periods=200):
        self.api_base_path = api_base_path
        self.max_periods = max_periods
        self.period = period
        if period not in ["minute", "hour", "day"]:
            raise ValueError("period has not the right value")




    def grab(self, crypto_name, modified_timebase=False):
        """
        Acquisition of all stock data for cypto_name.
        If modified_timebase is provided then the grabber will convert the result to asked candlesticks
        Possible values of modified_timebase:
            15minutes (from a minute based)
            1week (computed from hours)
            1month (computed from days)

        """


        if modified_timebase is not False:



            if modified_timebase == "15minutes":
                self.max_periods = 200 * 15
                self.period = "minute"
            elif modified_timebase == "1week":
                self.max_periods = 50 * 7
                self.period = "day"
            elif modified_timebase == "1month":
                self.max_periods = 20*30
                self.period = "day"


        r = requests.get(
            self.api_base_path + self.period + "?fsym={}&tsym=USD&limit={}&e=bitfinex".format(crypto_name.upper(),
                                                                                              self.max_periods))



        response = r.json()
        if r.status_code == 200 and response['Response'] != "Error":

            datas = pd.DataFrame(response["Data"]);
            # convert all data to numeric values
            datas = datas.apply(pd.to_numeric)

            volume = datas['volumeto']
            datas = datas.drop(columns=['volumeto', 'volumefrom'])
            datas['volume'] = pd.Series(volume, index=datas.index)

            if modified_timebase is not False:
                if modified_timebase == "15minutes":
                    n = 15
                    
                elif modified_timebase == "1week":
                    n = 7
                elif modified_timebase == "1month":
                    n = 30

                chunks = [datas[i:i+n] for i in range(0,datas.shape[0],n)]
                
                compressed_datas = pd.DataFrame(columns={'open','close','high','low','volume','time'})
                for chunk in chunks:
                    compressed_datas = compressed_datas.append({
                        'open':chunk.iloc[0]['open'],
                        'close':chunk.iloc[-1]['close'],
                        'high':chunk['high'].max(),
                        'low':chunk['low'].min(),
                        'volume':chunk['volume'].sum(),
                        'time':chunk.iloc[0]['time']
                        }, ignore_index=True)
                datas = compressed_datas

            print "Grabbed for {}".format(crypto_name)
            print "from\t{}".format(datetime.datetime.fromtimestamp(datas.iloc[0]['time']))
            print "to\t{}".format(datetime.datetime.fromtimestamp(datas.iloc[-1]['time']))
            return datas
        else:
            print "error grabbing {}".format(crypto_name)
            return False
