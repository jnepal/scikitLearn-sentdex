import pandas as pd
import os
import time
import matplotlib
import re
import matplotlib.pyplot as plt

from datetime import datetime

#Matplot lib style
matplotlib.style.use('dark_background')

path = "D:/financial-aid-investment/intraQuarter"

def keyStats(gather="Total Debt/Equity (mrq)"):
    statsPath = path+ '/_KeyStats'
    '''
        os.walk() returns dirpath , dirname and filename
        we want dirpath represented by index 0
    '''
    stockList = [x[0] for x in os.walk(statsPath)]
    dataFrame = pd.DataFrame(columns=['Date',
                                      'Unix',
                                      'Ticker',
                                      'DE Ratio',
                                      'Price',
                                      'stockPercentChange',
                                      'S&P500',
                                      'S&P500PercentChange',
                                      'Difference',
                                      'Trailing P/E',
                                      'Status'])

    sps500DataFrame = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")
    tickerList = []

    #stockList has first element as statsPath itself
    for eachDir in stockList[1:25]:
        '''listdir returns a list containing the names of the files in the directory.'''
        eachFile = os.listdir(eachDir)
        ticker = eachDir.split('\\')[1]
        tickerList.append(ticker)

        startingStockValue = False
        startingSP500Value = False

        if len(eachFile) > 0:
            for file in eachFile:
                dateStamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unixTime  = time.mktime(dateStamp.timetuple())
                fullFilePath = eachDir + '/' + file
                sourceFile   = open(fullFilePath, 'r').read()

                try:
                    try:
                        value = float(sourceFile.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except Exception as e:
                        try:
                            value = float(sourceFile.split(gather + ':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])
                        except Exception as e:
                            #Except due to N/A as value
                            pass
                    try:
                        sp500Date = datetime.fromtimestamp(unixTime).strftime('%Y-%m-%d')
                        row = sps500DataFrame[sps500DataFrame.index == sp500Date]
                        sp500Value = float(row["Adjusted Close"])

                    except Exception as e:
                        #make sure it's not value of weekend
                        #259200 s = 3 days

                        try:
                            sp500Date = datetime.fromtimestamp(unixTime - 259200).strftime('%Y-%m-%d')
                            row = sps500DataFrame[sps500DataFrame.index == sp500Date]
                            sp500Value = float(row["Adjusted Close"])
                        except Exception as e:
                            pass
                            # print(str(e), ticker, file)

                    try:
                        stockPrice = float(sourceFile.split('</small><big><b>')[1].split('</b></big>')[0])


                    except Exception as e:

                        try:
                            stockPrice = (sourceFile.split('</small><big><b>')[1].split('</b></big>')[0])
                            #\d{1,8} is digit from length 1 to 8
                            stockPrice = re.search(r'(\d{1,8}\.\d{1,8})', stockPrice)
                            stockPrice = float(stockPrice.group(1))

                        except Exception as e:
                            stockPrice = (sourceFile.split('<span class="time_rtq_ticker'">")[1].split('</span>')[0])
                            stockPrice = re.search(r'(\d{1,8}\.\d{1,8})', stockPrice)
                            stockPrice = float(stockPrice.group(1))

                    if not startingStockValue:
                        startingStockValue = stockPrice

                    if not startingSP500Value:
                        startingSP500Value = sp500Value

                    stockPercentChange = ((stockPrice - startingStockValue)/startingSP500Value) * 100
                    sp500PercentChange = ((sp500Value - startingSP500Value)/startingSP500Value) * 100

                    difference = stockPercentChange - sp500PercentChange

                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"

                    dataFrame  = dataFrame.append({'Date': dateStamp,
                                                   'Unix': unixTime,
                                                   'Ticker': ticker,
                                                   'DE Ratio': value,
                                                   'Price': stockPrice,
                                                   'stockPercentChange': stockPercentChange,
                                                   'S&P500': sp500Value,
                                                   'S&P500PercentChange': sp500PercentChange,
                                                   'Difference': difference,
                                                   'Status': status
                                                   }, ignore_index = True)

                except Exception as e:
                    pass
                    # print(str(e), ticker, file)

    for ticker in tickerList:
        try:
            plotDifference = dataFrame[(dataFrame['Ticker'] == ticker)]
            plotDifference = plotDifference.set_index(['Date'])

            if plotDifference['Status'][-1] == "underperform":
                color = 'r'
            else:
                color = 'g'

            plotDifference['Difference'].plot(label = ticker, color=color)
            plt.legend()
        except:
            pass

    plt.show()

    saveFile = gather.replace(' ', '').replace('/', '').replace('(', '').replace(')', '')+ '.csv'
    dataFrame.to_csv(saveFile)



keyStats()