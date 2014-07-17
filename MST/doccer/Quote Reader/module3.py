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

#new=numpy.zeros(5)
#print numpy.arange(4,26-2)


#x=numpy.arange(1,5)
#print x[24]

base1='https://in.finance.yahoo.com/lookup/stocks;_ylt=AsfadPlRuexIkRmGoJuQO499UblG;_ylu=X3oDMTFiM3RzMzF1BHBvcwMyBHNlYwN5ZmlTeW1ib2xMb29rdXBSZXN1bHRzBHNsawNzdG9ja3M-?s='
base2='&t=S&m=IN&r=&b='

opn=urllib2.urlopen(base1 + 'Z' + base2 + '3')                                 #change alphabet here
opn=opn.read()
strg=opn.split('</em></a></li></ul><div class')[1]
strg=strg.split('\n')[0]

print strg