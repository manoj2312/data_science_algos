'''
Created on May 27, 2014

@author: admin
'''

# This alternate version of z_1 reads data of all scrips whose quotes start with one letter when run once.

import urllib2
import string
import numpy

alphalist='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

base1='https://in.finance.yahoo.com/lookup/stocks;_ylt=AnYHkcuwL4JdpzpRuiNr87d4UblG;_ylu=X3oDMTFiY3J1ZmVhBHBvcwMyOARzZWMDeWZpU3ltYm9sTG9va3VwUmVzdWx0cwRzbGsDZmlyc3Q-?s='
base2='&t=S&m=IN&r=1&b='

file_open = open('quote_store', 'a')

for j in range(1):
# the scrips starting with the letter 'alpha'.
    alpha= 'I'#alphalist[j]

# 'base1 + alpha + base2 + '0'' is the url of the first page of the list of scrips starting with the letter 'alpha'.
# The following block crawls the page to find the number of scrips which start with 'alpha'.
    opn=urllib2.urlopen(base1 + alpha + base2 + '0')
    opn=opn.read()
    stkunt=opn.split('title="Stocks"><em>Stocks<br>')
    stkunt=stkunt[1].split(')')
    stkunt = int(stkunt[0].split('(')[1])

# each page stores 19 scrip names.    
    arr=numpy.arange((stkunt/20)+1)
    arr=20*arr
    page=range((stkunt/20)+1)
    
# each element in 'page' represents the url address of a new page on the website. 
#'new' is the list of all scrip names on that page and some stray &amp values.
    Listalpha = []        
    for i in range((stkunt/20)+1):
        page[i] = base1 + alpha + base2 + str(arr[i])
        opened=urllib2.urlopen(page[i])
        opened=opened.read()
        strg=opened.split('</em></a></li></ul><div class')[1]
        strg=strg.split('\n')[0]
        new=strg.split('?s=')

# There are several strays before the scrip names start and after the scrip names end. The number of these strays is indefinite
# The following flexible loop enables us to enter the if loop when the scrip names start and immediately terminate the whole process when the scrp names stop and strays start.
# 'togg' is initially 2 and remains greater than 2 when all initial strays are occurred. Once the scrip names start, the togg is maintained at 0 so the elif loop is never entered. However, when the later strays start occurring, togg is set at 1 and process ends.  
# 'Listalpha' is used to store all the scrip names.
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

                    
    # print Listalpha
    # print len(Listalpha)
                    
# Orderly storing of all data from 'Listalpha'                     
    file_open.write(alpha + '----------------' + '(' + str(len(Listalpha)) + ')' + '\n\n')
    for l in range(len(Listalpha)):
        file_open.write(Listalpha[l] + '\n')
                        
    file_open.write('\n\n')
    
file_open.close()
