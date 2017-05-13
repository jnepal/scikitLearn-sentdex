import numpy as np
import pandas as pd
import os
import time
import quandl

quandl.ApiConfig.api_key = "GbXL38EyoJxLfTtNXjnL"

# data = quandl.get("WIKI/KO", start_date = "2000-12-12", end_date = "2015-12-30")
#
# print(data)

path = "D:/financial-aid-investment/intraQuarter"

def stockPrices():
    dataFrame = pd.DataFrame()
    statsPath = path + "/_KeyStats"
    stockList = [x[0] for x in os.walk(statsPath)]


    for eachDir in stockList[1:]:
        try:
            ticker = eachDir.split("\\")[1]

            name = 'WIKI/' + ticker.upper()
            data = quandl.get(name,
                              start_date = "2000-12-12",
                              end_date = "2015-12-30")

            data[ticker.upper()] = data["Adj. Close"]
            dataFrame = pd.concat([dataFrame, data[ticker.upper()]], axis = 1)

        except Exception as e:
            print(str(e))

    dataFrame.to_csv('stockprices.csv')
stockPrices()