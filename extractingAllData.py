'''
    Not Sure why But the data saved by this script isnot accurate
    enough. Refer sentdex-extractingAllData.py
'''

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



def keyStats(gather=["Total Debt/Equity",
                      'Trailing P/E',
                      'Price/Sales',
                      'Price/Book',
                      'Profit Margin',
                      'Operating Margin',
                      'Return on Assets',
                      'Return on Equity',
                      'Revenue Per Share',
                      'Market Cap',
                      'Enterprise Value',
                      'Forward P/E',
                      'PEG Ratio',
                      'Enterprise Value/Revenue',
                      'Enterprise Value/EBITDA',
                      'Revenue',
                      'Gross Profit',
                      'EBITDA',
                      'Net Income Avl to Common ',
                      'Diluted EPS',
                      'Earnings Growth',
                      'Revenue Growth',
                      'Total Cash',
                      'Total Cash Per Share',
                      'Total Debt',
                      'Current Ratio',
                      'Book Value Per Share',
                      'Cash Flow',
                      'Beta',
                      'Held by Insiders',
                      'Held by Institutions',
                      'Shares Short (as of',
                      'Short Ratio',
                      'Short % of Float',
                      'Shares Short (prior ']):
    statsPath = path+ '/_KeyStats'


    '''
        os.walk() returns dirpath , dirname and filename
        we want dirpath represented by index 0
    '''
    stockList = [x[0] for x in os.walk(statsPath)]
    dataFrame = pd.DataFrame(columns=['Date',
                                      'Unix',
                                      'Ticker',
                                      'Price',
                                      'stockPercentChange',
                                      'S&P500',
                                      'S&P500PercentChange',
                                      'Difference',
                                      'DE Ratio',
                                      'Trailing P/E',
                                      'Price/Sales',
                                      'Price/Book',
                                      'Profit Margin',
                                      'Operating Margin',
                                      'Return on Assets',
                                      'Return on Equity',
                                      'Revenue Per Share',
                                      'Market Cap',
                                      'Enterprise Value',
                                      'Forward P/E',
                                      'PEG Ratio',
                                      'Enterprise Value/Revenue',
                                      'Enterprise Value/EBITDA',
                                      'Revenue',
                                      'Gross Profit',
                                      'EBITDA',
                                      'Net Income Avl to Common ',
                                      'Diluted EPS',
                                      'Earnings Growth',
                                      'Revenue Growth',
                                      'Total Cash',
                                      'Total Cash Per Share',
                                      'Total Debt',
                                      'Current Ratio',
                                      'Book Value Per Share',
                                      'Cash Flow',
                                      'Beta',
                                      'Held by Insiders',
                                      'Held by Institutions',
                                      'Shares Short (as of',
                                      'Short Ratio',
                                      'Short % of Float',
                                      'Shares Short (prior ',
                                      'Status'])

    sps500DataFrame = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")
    tickerList = []

    #stockList has first element as statsPath itself
    for eachDir in stockList[1:]:
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
                    valueList = []

                    for eachGather in gather:
                        try:

                            #we need to escape because we have characters like % in list
                            regex = re.escape(eachGather) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                            # regex = re.escape(eachGather) + r'.*?(\d{1,8}\.\d{1,8}M?B?K?|N/A)%?</td>'
                            value = re.search(regex, sourceFile)
                            value = value.group(1)


                            if "B" in value:
                                value = float(value.replace("B", ''))*1000000000

                            elif "M" in value:
                                value = float(value.replace("M", ''))*1000000

                            elif "K" in value:
                                value = float(value.replace("K", ''))*1000





                            valueList.append(value)


                        except Exception as e:
                            value = "N/A"
                            valueList.append(value)



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

                    if valueList.count("N/A")>0:
                        pass
                    else:
                        dataFrame  = dataFrame.append({'Date': dateStamp,
                                                       'Unix': unixTime,
                                                       'Ticker': ticker,
                                                       'Price': stockPrice,
                                                       'stockPercentChange': stockPercentChange,
                                                       'S&P500': sp500Value,
                                                       'S&P500PercentChange': sp500PercentChange,
                                                       'Difference': difference,
                                                       'DE Ratio':valueList[0],
                                                      #'Market Cap':valueList[1],
                                                       'Trailing P/E':valueList[1],
                                                       'Price/Sales':valueList[2],
                                                       'Price/Book':valueList[3],
                                                       'Profit Margin':valueList[4],
                                                       'Operating Margin':valueList[5],
                                                       'Return on Assets':valueList[6],
                                                       'Return on Equity':valueList[7],
                                                       'Revenue Per Share':valueList[8],
                                                       'Market Cap':valueList[9],
                                                       'Enterprise Value':valueList[10],
                                                       'Forward P/E':valueList[11],
                                                       'PEG Ratio':valueList[12],
                                                       'Enterprise Value/Revenue':valueList[13],
                                                       'Enterprise Value/EBITDA':valueList[14],
                                                       'Revenue':valueList[15],
                                                       'Gross Profit':valueList[16],
                                                       'EBITDA':valueList[17],
                                                       'Net Income Avl to Common ':valueList[18],
                                                       'Diluted EPS':valueList[19],
                                                       'Earnings Growth':valueList[20],
                                                       'Revenue Growth':valueList[21],
                                                       'Total Cash':valueList[22],
                                                       'Total Cash Per Share':valueList[23],
                                                       'Total Debt':valueList[24],
                                                       'Current Ratio':valueList[25],
                                                       'Book Value Per Share':valueList[26],
                                                       'Cash Flow':valueList[27],
                                                       'Beta':valueList[28],
                                                       'Held by Insiders':valueList[29],
                                                       'Held by Institutions':valueList[30],
                                                       'Shares Short (as of':valueList[31],
                                                       'Short Ratio':valueList[32],
                                                       'Short % of Float':valueList[33],
                                                       'Shares Short (prior ':valueList[34],
                                                       'Status': status
                                                       }, ignore_index = True)

                except Exception as e:
                    pass
                    # print(str(e), ticker, file)

    # for ticker in tickerList:
    #     try:
    #         plotDifference = dataFrame[(dataFrame['Ticker'] == ticker)]
    #         plotDifference = plotDifference.set_index(['Date'])
    #
    #         if plotDifference['Status'][-1] == "underperform":
    #             color = 'r'
    #         else:
    #             color = 'g'
    #
    #         plotDifference['Difference'].plot(label = ticker, color=color)
    #         plt.legend()
    #     except:
    #         pass
    #
    # plt.show()
    # print(dataFrame)

    dataFrame.to_csv('keyStats.csv')



keyStats()
