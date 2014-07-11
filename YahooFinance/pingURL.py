import socket
import urllib
from dataParser import parseData
import copy
import numpy

socket.setdefaulttimeout(100000)  # timeout in seconds

def constructURL(Symbol, fromDay, fromMonth, fromYear, toDay, toMonth, toYear, tradingPeriod):
    urlBaseString='http://ichart.yahoo.com/table.csv?'
    symbolBaseString='s='
    fromMonthBaseString='&a='
    fromDayBaseString='&b='
    fromYearBaseString='&c='
    toMonthBaseString='&d='
    toDayBaseString='&e='
    toYearBaseString='&f='
    tradingPeriodBaseString='&g='
       
    symbolString = symbolBaseString + Symbol
    fromDayString = fromDayBaseString + str(fromDay)
    fromMonthString = fromMonthBaseString + str(fromMonth-1)
    fromYearString = fromYearBaseString + str(fromYear)
    toDayString = toDayBaseString + str(toDay)
    toMonthString = toMonthBaseString + str(toMonth-1)
    toYearString = toYearBaseString + str(toYear)
    tradingPeriodString = tradingPeriodBaseString + tradingPeriod
    endUrlString = '&ignore=.csv'
    # url = 'http://ichart.yahoo.com/table.csv?s=GOOG&a=0&b=1&c=2000&d=0&e=31&f=2010&g=d&ignore=.csv'
    url=urlBaseString + symbolString + fromMonthString + fromDayString + fromYearString+ toMonthString + toDayString  + toYearString + tradingPeriodString + endUrlString
    return url

def pingUrl(url):
    Count=1
    dataRead=[]
    while Count<10:
        try :
            response = urllib.request.urlopen( url )
            dataRead = response.read()
        except urllib.error.HTTPError, e:
            print('The server couldn\'t fulfill the request. Reason:', str(e.code))
            Count=copy.deepcopy(Count+1)
        except urllib.error.URLError, e:
            print('We failed to reach a server. Reason:', str(e.reason))
            Count=copy.deepcopy(Count+1)
        else :
            html = response.read()
            print('got response!')
            Count=11
    return Count, dataRead