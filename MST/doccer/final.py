'''
Created on May 27, 2014

@author: admin
'''
import urllib2
import string
import numpy

alphalist='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for j in range(26):

    alpha= alphalist[j]

    base1='https://in.finance.yahoo.com/lookup/stocks;_ylt=AsfadPlRuexIkRmGoJuQO499UblG;_ylu=X3oDMTFiM3RzMzF1BHBvcwMyBHNlYwN5ZmlTeW1ib2xMb29rdXBSZXN1bHRzBHNsawNzdG9ja3M-?s='
    base2='&t=S&m=IN&r=&b='

    opn=urllib2.urlopen(base1 + alpha + base2 + '0')
    opn=opn.read()
    stkunt=opn.split('title="Stocks"><em>Stocks<br>')
    stkunt=stkunt[1].split(')')
    stkunt = int(stkunt[0].split('(')[1])
    
    
    arr=numpy.arange((stkunt/20)+1)
    arr=20*arr
    
    page=range((stkunt/20)+1)
    
    Listalpha = []
    
    
    for i in range((stkunt/20)+1):
        page[i] = base1 + alpha + base2 + str(arr[i])
        opened=urllib2.urlopen(page[i])
        opened=opened.read()
        strg=opened.split('</em></a></li></ul><div class')[1]
        strg=strg.split('\n')[0]
        new=strg.split('?s=')
        
        
        for k in numpy.arange(4,len(new)):
            if((new[k][0]==alpha) & (new[k][1]!='&')):
                temp=new[k].split('</a></td><td>')    
                temp=temp[0].split('">')[0]                                                       
                Listalpha.append(temp)
                    
                    
    #print Listalpha
    #print len(Listalpha)
                    
    file_open = open('quote_store', 'a')
                    
    file_open.write(alpha + '----------------' + '(' + str(len(Listalpha)) + ')' + '\n\n')
    for l in range(len(Listalpha)):
        file_open.write(Listalpha[l] + '\n')
                        
    file_open.write('\n\n')
