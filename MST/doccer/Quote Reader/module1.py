'''
Created on May 26, 2014

@author: admin
'
'''
import numpy
import sklearn
import webbrowser
import urllib2
import sre
import HTMLParser
import htmllib
import string

#base1='https://in.finance.yahoo.com/lookup/stocks;_ylt=AsfadPlRuexIkRmGoJuQO499UblG;_ylu=X3oDMTFiM3RzMzF1BHBvcwMyBHNlYwN5ZmlTeW1ib2xMb29rdXBSZXN1bHRzBHNsawNzdG9ja3M-?s='
#base2='&t=S&m=IN&r=&b='

#arr=numpy.arange(2033)
#arr=20*arr

#page=range(2033)
#for i in range(2033):
#    page[i] = base1 + 'A' + base2 + str(arr[i])

    opened=urllib2.urlopen(page[i])
    opened=opened.read()
    str=opened.split('</em></a></li></ul><div class')[1]
    str=str.split('\n')[0]
    new=str.split('?s=')
    
    
    for k in range(len(new)-3):
        if(k>3):
            temp=new[k].split('</a></td><td>')
            temp=temp[0].split('">')[0]
            ListA.append(temp)
            
            
print ListA




