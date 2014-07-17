'''
Created on Jun 16, 2014

@author: admin
'''
import urllib2
import string
import numpy
import csv

# names of scrips whose data is to be downloaded are read from 'Mean_Reversion_strategy_data_PRICES.csv' into the list 'k'.
with open('Mean_Reversion_strategy_data_PRICES.csv','rb') as f:
    rdr=csv.reader(f)
    k=[]
    for row in rdr:
        k.append(row[0])
k=k[1:]


# 'kat' is a list which stores all scrips whose data is available on yahoo finance in any of nse or bse.
# 'quote_store' is a file containing all the scrip names whose data is available on yahoo finance. This file was created by crawling the website. Names are stored alphabetically.
# 'b' takes 0 or 1 depending on whether the scrip from k is available in 'quote_store'.
kat=[]
counter=0
for i in range(len(k)):
    fila = open('quote_store','r')
    b=0
    for liner in fila:
        if( (k[i]+'.BO'==liner[:-1]) | (k[i]+'.NS'==liner[:-1]) ):
            kat.append(liner[:-1])
            b=1
    counter=counter+b
print 'number of unique scrips whose data is available: ' + str(counter)



alpha=[]
for i in range(len(k)):
    if(k[i][0]=='I'):
        alpha.append(k[i])

#===============================================================================
# 
#===============================================================================

x=1
base1='https://in.finance.yahoo.com/lookup/stocks;_ylt=AsfadPlRuexIkRmGoJuQO499UblG;_ylu=X3oDMTFiM3RzMzF1BHBvcwMyBHNlYwN5ZmlTeW1ib2xMb29rdXBSZXN1bHRzBHNsawNzdG9ja3M-?s='
base2='&t=S&b=0&m=IN'

#file_open = open('quote_store', 'a')

for j in range(len(alpha)):
    new=[]
    page = base1 + alpha[j] + base2
    opn=urllib2.urlopen(page)
    opn=opn.read()
    stkunt=opn.split('title="Stocks"><em>Stocks<br>')
    stkunt=stkunt[1].split(')')
    stkunt = int(stkunt[0].split('(')[1]) 
    print stkunt
     
    strg=opn.split('</em></a></li></ul><div class')[1]
    strg=strg.split('\n')[0]
    new=strg.split('='+alpha[j])
    new=new[1:]
    for i in range(len(new)):
        new[i] = new[i].split('</a></td><td>')[0]
        new[i] = new[i].split('>')[1]
    
    for i in range(len(new)):
        b=0
        if( (new[i][:len(alpha[j])+3]==alpha[j]+'.BO') | (new[i][:len(alpha[j])+3]==alpha[j]+'.NS') ):
            kat.append(new[i])
            b=1
        a=a+b
        
#file_open.close()
print kat
print len(kat)
print a
