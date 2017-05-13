import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import statistics

from sklearn import svm, preprocessing

#Matplot lib style
matplotlib.style.use('ggplot')

features =  ['DE Ratio',
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
             'Shares Short (prior ']

def buildDataSet():

    # dataFrame = pd.DataFrame.from_csv('key_stats_accurate_performance_WITH_NA.csv')
    dataFrame = pd.DataFrame.from_csv('key_stats_accurate_performance_WITH_NA.csv')
    # dataFrame = dataFrame[:100]

    #Randomising Data Frame
    dataFrame = dataFrame.reindex(np.random.permutation(dataFrame.index))

    #NAN : not a number pandas lib
    dataFrame = dataFrame.replace("NAN", 0).replace("N/A", 0)


    X = np.array(dataFrame[features].values)

    #Multiple column select pandas feature: write all columns as list
    Z = np.array(dataFrame[["stock_p_change", "sp500_p_change"]])

    #preprocessing data
    X = preprocessing.scale(X)

    y = (dataFrame["Status"]
         .replace("underperform", 0)
         .replace("outperform", 1)
         .values.tolist())

    return X, y, Z

def analysis():
    '''
     Trade cost , Interest of Banks etc Not Accounted
    '''
    testSize = 1500
    investAmount = 10000
    totalInvest  = 0
    ifMarket = 0 #money made if invested according to market change i.e with accordance with S&P 500
    ifStrategy = 0 #money made if invested according to our strategy

    X, y, Z = buildDataSet()

    # #shuffling data
    # np.random.shuffle(X)
    # np.random.shuffle(y)

    print(len(X))

    #clasifier
    clf = svm.SVC(kernel = 'linear', C = 1.0)
    clf.fit(X[:-testSize], y[:-testSize])

    correctCount = 0

    for x in range(1, testSize+1):
        if clf.predict(X[-x])[0] == y[-x]:
            correctCount += 1

        if clf.predict(X[-x])[0] == 1:
            investReturn = investAmount + investAmount * (Z[-x][0]/100)
            marketReturn = investAmount + investAmount * (Z[-x][1]/100)

            totalInvest += 1
            ifMarket    += marketReturn
            ifStrategy  += investReturn


    print("Accuracy :", (correctCount/testSize))

    print("Total Trades :", totalInvest)
    print("Ending With Strategy :", ifMarket)
    print("Ending With Market :", ifMarket)

    comparision = ((ifStrategy - ifMarket) / ifMarket ) * 100

    print("Compared to market, We earned", str(comparision) + "% more")
    # print("Average Investment Return")

    #What we have not invested any money
    #no bank interest added (makes no sense though)

    amountIfNotInvested =  totalInvest * investAmount

    avgMarketReturn   = ((ifMarket - amountIfNotInvested) / amountIfNotInvested) * 100
    avgStrategyReturn = ((ifStrategy - amountIfNotInvested) / amountIfNotInvested) * 100

    print("Average Market Investment Return :", str(avgMarketReturn) + "%")
    print("Average Strategy Investment Return :", str(avgStrategyReturn) + "%")


    ''' For Graphing Purpose '''
    # #coefficient
    # w  = clf.coef_[0]
    # a  = -w[0] / w[1]
    #
    # xx = np.linspace(min(X[:, 0]), max(X[:, 1]))
    # yy = a * xx - clf.intercept_[0] / w[1]
    #
    # #k- represents black solid line
    # h0 = plt.plot(xx, yy , "k-", label = "non weighted")
    #
    # plt.scatter(X[:, 0], X[:, 1], c=y)
    # plt.ylabel("Trailing P/E")
    # plt.xlabel("DE Ratio")
    # plt.legend()
    # plt.show()

analysis()
