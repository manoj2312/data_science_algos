'''
Created on Jun 16, 2014

@author: admin
'''

# This sub-code'ss purpose: to filter all stocks that are already available and also available on yahoo-finance.
# The end result: a list 'kat' consisting of all the requiored stock quotes.
# kat = ['ARVIND.BO', 'ARVIND.NS', 'DISHTV.BO', 'DISHTV.NS', 'HINDZINC.BO', 'HINDZINC.NS', 'WIPRO.BO', 'WIPRO.NS', 'ACC.BO', 'ACC.NS', 'ALBK.NS', 'AMBUJACEM.NS', 'ANDHRABANK.BO', 'APOLLOTYRE.BO', 'ASHOKLEY.BO', 'ASHOKLEY.NS', 'AXISBANK.NS', 'BANKINDIA.NS', 'BATAINDIA.NS', 'BHEL.BO', 'BHEL.NS', 'BPCL.BO', 'BPCL.NS', 'BIOCON.NS', 'CESC.BO', 'CESC.NS', 'CAIRN.NS', 'CANBK.NS', 'CIPLA.BO', 'CIPLA.NS', 'COLPAL.NS', 'DLF.NS', 'DABUR.BO', 'DABUR.NS', 'DIVISLAB.BO', 'DIVISLAB.NS', 'DRREDDY.BO', 'DRREDDY.NS', 'EXIDEIND.BO', 'EXIDEIND.NS', 'GAIL.BO', 'GAIL.NS', 'GMRINFRA.NS', 'GODREJIND.NS', 'GRASIM.BO', 'GRASIM.NS', 'HCLTECH.BO', 'HCLTECH.NS', 'HDFCBANK.BO', 'HDFCBANK.NS', 'HAVELLS.NS', 'HEXAWARE.BO', 'HEXAWARE.NS', 'HINDALCO.BO', 'HINDALCO.NS', 'HINDPETRO.NS', 'HDIL.NS', 'HDFC.BO', 'HDFC.NS', 'JSWSTEEL.NS', 'JPPOWER.BO', 'JPPOWER.NS', 'KTKBANK.NS', 'KOTAKBANK.BO', 'KOTAKBANK.NS', 'LICHSGFIN.BO', 'LICHSGFIN.NS', 'MRF.NS', 'MARUTI.BO', 'MARUTI.NS', 'NMDC.NS', 'NTPC.BO', 'NTPC.NS', 'ONGC.BO', 'ONGC.NS', 'OFSS.NS', 'PTC.BO', 'PTC.NS', 'PETRONET.NS', 'PFC.NS', 'POWERGRID.NS', 'PNB.BO', 'PNB.NS', 'RANBAXY.BO', 'RANBAXY.NS', 'RCOM.BO', 'RCOM.NS', 'RELIANCE.NS', 'RELINFRA.BO', 'RELINFRA.NS', 'RPOWER.NS', 'RECLTD.BO', 'RECLTD.NS', 'SSLT.BO', 'SIEMENS.BO', 'SIEMENS.NS', 'SBIN.NS', 'SAIL.BO', 'SAIL.NS', 'SUNPHARMA.BO', 'SUNPHARMA.NS', 'SUNTV.NS', 'SYNDIBANK.BO', 'SYNDIBANK.NS', 'TATACHEM.BO', 'TATACHEM.NS', 'TATACOMM.BO', 'TATACOMM.NS', 'TCS.BO', 'TCS.NS', 'TATAPOWER.BO', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.BO', 'TITAN.NS', 'UCOBANK.NS', 'UNIONBANK.BO', 'UNIONBANK.NS', 'UNITECH.NS', 'UPL.BO', 'VOLTAS.BO', 'VOLTAS.NS', 'YESBANK.NS', 'ZEEL.NS', 'IOC.NS', 'IOC.BO', 'ICICIBANK.NS', 'ICICIBANK.BO', 'IDBI.BO', 'IDBI.NS', 'IDFC.NS', 'IDFC.BO', 'IFCI.BO', 'IFCI.NS', 'ITC.NS', 'ITC.BO', 'IDEA.NS', 'INDIACEM.NS', 'INDIACEM.BO', 'IBREALEST.NS', 'IBREALEST.BO', 'IOB.NS', 'IOB.BO', 'IGL.NS', 'IGL.BO', 'INFY.NS']


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
        if( (k[i]+'.BO'==liner[:-2]) | (k[i]+'.NS'==liner[:-2]) ):
            kat.append(liner[:-2])
            b=1
    counter=counter+b

print 'number of unique scrips whose data is available: ' + str(counter)


# 'alpha' is the list which stores all scrip names from data already available that start with 'I'.
# all the code that follows adds the data of the scrips which start with 'I'. This extra effort for 'I' is done because none of the scrips starting with 'I' were read into quote store. 
alpha=[]
for i in range(len(k)):
    if(k[i][0]=='I'):
        alpha.append(k[i])

x=1
base1='https://in.finance.yahoo.com/lookup/stocks;_ylt=AsfadPlRuexIkRmGoJuQO499UblG;_ylu=X3oDMTFiM3RzMzF1BHBvcwMyBHNlYwN5ZmlTeW1ib2xMb29rdXBSZXN1bHRzBHNsawNzdG9ja3M-?s='
base2='&t=S&b=0&m=IN'
#-------------------------------------------------------------- print len(alpha)
for j in range(len(alpha)):
    new=[]
    page = base1 + alpha[j] + base2
    opn=urllib2.urlopen(page)
    opn=opn.read()
    #===========================================================================
    # stkunt=opn.split('title="Stocks"><em>Stocks<br>')
    # stkunt=stkunt[1].split(')')
    # stkunt = int(stkunt[0].split('(')[1]) 
    # print stkunt
    #===========================================================================
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
        counter=counter+b
        

#--------------------------------------------------------------------- print kat
#---------------------------------------------------------------- print len(kat)
#----------------------------------------------------------------- print counter



