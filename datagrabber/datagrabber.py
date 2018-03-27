"""
Datagrabber class responsible for the fetching of historical cryptocurrency stock data.
"""
import requests
import pandas as pd



class DataGrabber:
    """

    """
    def __init__(self, period, api_base_path="https://min-api.cryptocompare.com/data/histo", max_periods=200):
        self.api_base_path = api_base_path
        self.max_periods = max_periods
        self.period = period
        if period  not in ["minute", "hour", "day"]:
            raise ValueError("period has not the right value")



    def grab(self,crypto_name):
        """
        Acquisition of all stock data for cypto_name.
        """
        r = requests.get(self.api_base_path+self.period+"?fsym={}&tsym=USD&limit={}".format(crypto_name.upper(),self.max_periods))


        response = r.json()
        if r.status_code==200 and response['Response']!="Error":
            
            datas = pd.DataFrame(response["Data"]);
            #convert all data to numeric values
            datas = datas.apply(pd.to_numeric)

            volume = datas['volumeto']
            datas = datas.drop(columns=['volumeto','volumefrom'])
            datas['volume'] = pd.Series(volume, index=datas.index)


            print "Grabbed for {}".format(crypto_name)
            return datas
        else:
            print "error grabbing {}".format(crypto_name)
            return False