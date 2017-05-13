import urllib.request
import os
import time

path = "D:/financial-aid-investment/intraQuarter"

def checkYahoo():
    statsPath = path + "/_KeyStats"
    stockList = [x[0] for x in os.walk(statsPath)]

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    for ticker in stockList:

        try:
            ticker = ticker.replace("D:/financial-aid-investment/intraQuarter/_KeyStats\\", "")
            link   = "http://finance.yahoo.com/quote/"+ticker.upper()+"/key-statistics"

            request  = urllib.request.Request(link, headers = headers)
            response = urllib.request.urlopen(request).read()

            savePath  = path+"/forward/"+str(ticker)+".html"
            store = open(savePath, 'w')
            store.write(str(response))
            store.close()

        except Exception as e:
            print(str(e))
            time.sleep(2)

checkYahoo()


