from pingURL import constructURL, pingUrl
from dataParser import getSymbols, parseData
import time

tic = time.clock()
path=["/home/manu/Documents/YahooFinance/VolumeLeadersBSE", "/home/manu/Documents/YahooFinance/VolumeLeadersNSE", "/home/manu/Documents/YahooFinance/GainersBSE","/home/manu/Documents/YahooFinance/GainersNSE","/home/manu/Documents/YahooFinance/LosersBSE","/home/manu/Documents/YahooFinance/LosersNSE"]
Symbols,Names = getSymbols(path)
# Current dates 1/1/2000 until 31/1/2010. 
print(len(Symbols))
Stocks=[]
Prices=[]
Dates=[]
for i in range(len(Symbols)):
#     time.sleep(2)
    Symbol=Symbols[i]
    fromDay=1
    fromMonth=1
    fromYear=2000
    toDay=17
    toMonth=2
    toYear=2014
    tradingPeriod='d'               # d=daily, w=weekly, m=monthly
    url = constructURL(Symbol, fromDay, fromMonth, fromYear, toDay, toMonth, toYear, tradingPeriod)
    count, data = pingUrl(url)
    Count, Date, adjClose = parseData(count, data)
    if Count==11:
        Stocks.append(Names[i])
        Prices.append(adjClose)
        Dates.append(Date)
    print(Names[i])
    toc = time.clock()
    print(toc - tic)
       
print(data)