import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

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

    dataFrame = pd.DataFrame.from_csv('key_stats.csv')
    # dataFrame = dataFrame[:100]

    #Randomising Data Frame
    dataFrame = dataFrame.reindex(np.random.permutation(dataFrame.index))

    X = np.array(dataFrame[features].values)


    #preprocessing data
    X = preprocessing.scale(X)

    y = (dataFrame["Status"]
         .replace("underperform", 0)
         .replace("outperform", 1)
         .values.tolist())

    return X, y

def analysis():

    testSize = 1500
    X, y = buildDataSet()

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
    print("Accuracy :", (correctCount/testSize))


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
