'''
Created on May 27, 2014

@author: admin
'''
import urllib2
import string
import numpy

x=1

alphalist='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

base1='https://in.finance.yahoo.com/lookup/stocks;_ylt=AnYHkcuwL4JdpzpRuiNr87d4UblG;_ylu=X3oDMTFiY3J1ZmVhBHBvcwMyOARzZWMDeWZpU3ltYm9sTG9va3VwUmVzdWx0cwRzbGsDZmlyc3Q-?s='
base2='&t=S&m=IN&r=1&b='

file_open = open('quote_store', 'a')

for j in range(1):

    alpha= 'I'#alphalist[j]

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
        
        togg=2
        for k in numpy.arange(4,len(new)):
            togg=togg+1
            if((new[k][0]==alpha)&(new[k][1:5]!='&amp')):
                temp=new[k].split('</a></td><td>')    
                temp=temp[0].split('">')[0]                                                       
                Listalpha.append(temp)
                togg=0
            elif(togg==1):
                break

                    
    #print Listalpha
    #print len(Listalpha)
                    
                    
    file_open.write(alpha + '----------------' + '(' + str(len(Listalpha)) + ')' + '\n\n')
    for l in range(len(Listalpha)):
        file_open.write(Listalpha[l] + '\n')
                        
    file_open.write('\n\n')
    
file_open.close()
