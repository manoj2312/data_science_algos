'''
Created on May 27, 2014

@author: admin
'''
import sklearn
import webbrowser
import urllib2
import sre
import HTMLParser
import htmllib
import string
import numpy

base1='https://in.finance.yahoo.com/lookup/stocks;_ylt=AsfadPlRuexIkRmGoJuQO499UblG;_ylu=X3oDMTFiM3RzMzF1BHBvcwMyBHNlYwN5ZmlTeW1ib2xMb29rdXBSZXN1bHRzBHNsawNzdG9ja3M-?s='
base2='&t=S&m=IN&r=&b='


open=urllib2.urlopen(base1 + 'A' + base2 + '0')
open=open.read()
stkunt=open.split('title="Stocks"><em>Stocks<br>')
stkunt=stkunt[1].split(')')
stkunt = stkunt[0].split('(')[1]
print int(stkunt)
    

