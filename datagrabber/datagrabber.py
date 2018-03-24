"""
Datagrabber class responsible for the fetching of historical cryptocurrency stock data.
"""
import requests
import pandas as pd


class DataGrabber:
    """

    """
    def __init__(self, api_base_path, period, max_periods):
        self.api_base_path = api_base_path
        self.max_periods = max_periods
        self.period = period
        if period is not in ["minute", "hour", "day"]:
            raise ValueError("period has not the right value")



    def grab():
        """
        Acquisition of all needed cruptocurency stock data from API.
        First we select only markets above 500k/24h
        """
        r = requests.get('')



    def parse():
