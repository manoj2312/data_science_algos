from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import webbrowser
import urllib
import urllib2
import re
import HTMLParser
import htmllib
import string
import numpy
import csv
import os
import subprocess
from scipy import linalg as lin
from matplotlib.pylab import plot
from matplotlib.pylab import show
#===============================================================================
# alpha= 'X'
# 
# base1='https://in.finance.yahoo.com/lookup/stocks;_ylt=AnYHkcuwL4JdpzpRuiNr87d4UblG;_ylu=X3oDMTFiY3J1ZmVhBHBvcwMyOARzZWMDeWZpU3ltYm9sTG9va3VwUmVzdWx0cwRzbGsDZmlyc3Q-?s='
# base2='&t=S&m=IN&r=1&b='
# 
# opn=urllib2.urlopen(base1 + alpha + base2 + '0')
# opn=opn.read()
# stkunt=opn.split('title="Stocks"><em>Stocks<br>')
# stkunt=stkunt[1].split(')')
# stkunt = int(stkunt[0].split('(')[1])
# 
# 
# arr=numpy.arange((stkunt/20)+1)
# arr=20*arr
# 
# page=range((stkunt/20)+1)
# 
# Listalpha = []
# 
# 
# for i in range((stkunt/20)+1):
#     page[i] = base1 + alpha + base2 + str(arr[i])
#     opened=urllib2.urlopen(page[i])
#     opened=opened.read()
#     strg=opened.split('</em></a></li></ul><div class')[1]
#     strg=strg.split('\n')[0]
#     new=strg.split('?s=')
#     
#     togg=2
#     for k in numpy.arange(4,len(new)):
#         togg=togg+1
#         if((new[k][1:5]!='&amp')&(new[k][0]==alpha)):
#             temp=new[k].split('</a></td><td>')    
#             temp=temp[0].split('">')[0]                                                       
#             Listalpha.append(temp)
#             togg=0
#         elif(togg==1):
#             break
#             
# print Listalpha
# print len(Listalpha)
# 
# file_open = open('quote_store', 'a')
# 
# file_open.write(alpha + '----------------' + '\n\n')
# for l in range(len(Listalpha)):
#     file_open.write(Listalpha[l] + '\n')
#     
# file_open.write('\n\n')
#===============================================================================

#===============================================================================
# page = 'https://ichart.finance.yahoo.com/table.csv?s=SBI.BO&d=4&e=26&f=2014&g=d&a=0&b=3&c=2000&ignore=.csv'
# opn=urllib2.urlopen(page)
# opn=opn.read()
# print opn.split('\n')[1]
#===============================================================================

#===============================================================================
# def feb(yr):
#     if((yr%4)==0):
#         return 29
#     else:
#         return 28
#       
#       
# year=2000
# month=0
# day=2
# date=[]
#   
# def monthlist(yr):
#     return [31,feb(yr),31,30,31,30,31,31,30,31,30,31]
#   
# def mop(num):
#     if(num<10):
#         return '0'+str(num) 
#     else:
#         return str(num)
#       
# def dator(yr,mn,dy):
#     return str(yr) + '-' + mop(mn) + '-' + mop(dy)
#       
#       
# for j in range(753):
#     for i in range(5):
#         if(day<monthlist(year)[month]):
#             day=day+1
#             date.append( dator(year,month+1,day) ) 
#         elif( (day>=monthlist(year)[month]) & (month<11) ):
#             day=day-monthlist(year)[month] + 1
#             month=month+1
#             date.append( dator(year,month+1,day) )
#         else:
#             day=day-monthlist(year)[month] + 1
#             month=0
#             year=year+1
#             date.append( dator(year,month+1,day) )
#     day=day+2        
#   
# 
#  
# file_open = open('yawho.csv','w')
# file_open.write('Date' + ',')
# for i in range(len(date)):
#     file_open.write(date[i] + ',')
# file_open.write('\n')
# file_open.close()
#  
# kat=['SBI.BO','ITC.BO']
# holadd=0
# 
# print len(date)
# for i in range(2):
#     store=numpy.zeros(len(date))
#     page = 'https://ichart.finance.yahoo.com/table.csv?s=' + kat[i] + '&d=4&e=26&f=2014&g=d&a=0&b=3&c=2000&ignore=.csv'
#     opn=urllib2.urlopen(page)
#     opn=opn.read()
#     row=opn.split('\n')
#     print len(row)
#     for j in range(2,len(row)):
#         liner = row[-j].split(',')
#         while(1):
#             if(liner[0]==date[j+holadd-2]):
#                 store[j+holadd-2]=liner[4]
#                 break
#             elif(holadd<len(date)+1-j):
#                 holadd=holadd+1
#             else:
#                 holadd=0
#                 break
#     
#     file_open = open('yawho.csv','a')
#     file_open.write('\n')
#     file_open.write(kat[i] + ',')
#     for j in range(len(store)):
#         file_open.write(str(store[j]) + ',')
#     file_open.close()
# 
#     print store
#     
#===============================================================================

#===============================================================================
# kat=['ARVIND.BO', 'ARVIND.NS', 'DISHTV.BO', 'DISHTV.NS', 'HINDZINC.BO', 'HINDZINC.NS', 'WIPRO.BO', 'WIPRO.NS', 'ACC.BO', 'ACC.NS', 'ALBK.NS', 'AMBUJACEM.NS', 'ANDHRABANK.BO', 'APOLLOTYRE.BO', 'ASHOKLEY.BO', 'ASHOKLEY.NS', 'AXISBANK.BO', 'AXISBANK.NS', 'BANKINDIA.NS', 'BATAINDIA.NS', 'BHARATFORG.BO', 'BHEL.BO', 'BHEL.NS', 'BPCL.BO', 'BPCL.NS', 'BHARTIARTL.BO', 'BIOCON.BO', 'BIOCON.NS', 'CESC.BO', 'CESC.NS', 'CAIRN.BO', 'CAIRN.NS', 'CANBK.NS', 'CENTURYTEX.BO', 'CIPLA.BO', 'CIPLA.NS', 'COLPAL.NS', 'DLF.BO', 'DLF.NS', 'DABUR.BO', 'DABUR.NS', 'DIVISLAB.BO', 'DIVISLAB.NS', 'DRREDDY.BO', 'DRREDDY.NS', 'EXIDEIND.BO', 'EXIDEIND.NS', 'GAIL.BO', 'GAIL.NS', 'GMRINFRA.BO', 'GMRINFRA.NS', 'GODREJIND.BO', 'GODREJIND.NS', 'GRASIM.BO', 'GRASIM.NS', 'HCLTECH.BO', 'HCLTECH.NS', 'HDFCBANK.BO', 'HDFCBANK.NS', 'HAVELLS.BO', 'HAVELLS.NS', 'HEROMOTOCO.BO', 'HEXAWARE.BO', 'HEXAWARE.NS', 'HINDALCO.BO', 'HINDALCO.NS', 'HINDPETRO.NS', 'HDIL.BO', 'HDIL.NS', 'HDFC.BO', 'HDFC.NS', 'JSWSTEEL.NS', 'JPPOWER.BO', 'JPPOWER.NS', 'KTKBANK.BO', 'KTKBANK.NS', 'KOTAKBANK.BO', 'KOTAKBANK.NS', 'LICHSGFIN.BO', 'LICHSGFIN.NS', 'MRF.BO', 'MRF.NS', 'MARUTI.BO', 'MARUTI.NS', 'NMDC.NS', 'NTPC.BO', 'NTPC.NS', 'ONGC.BO', 'ONGC.NS', 'OFSS.NS', 'PTC.BO', 'PTC.NS', 'PETRONET.BO', 'PETRONET.NS', 'PFC.BO', 'PFC.NS', 'POWERGRID.BO', 'POWERGRID.NS', 'PNB.BO', 'PNB.NS', 'RANBAXY.BO', 'RANBAXY.NS', 'RCOM.BO', 'RCOM.NS', 'RELIANCE.NS', 'RELINFRA.BO', 'RELINFRA.NS', 'RPOWER.BO', 'RPOWER.NS', 'RECLTD.BO', 'RECLTD.NS', 'SSLT.BO', 'SIEMENS.BO', 'SIEMENS.NS', 'SBIN.NS', 'SAIL.BO', 'SAIL.NS', 'SUNPHARMA.BO', 'SUNPHARMA.NS', 'SUNTV.BO', 'SUNTV.NS', 'SYNDIBANK.BO', 'SYNDIBANK.NS', 'TATACHEM.BO', 'TATACHEM.NS', 'TATACOMM.BO', 'TATACOMM.NS', 'TCS.BO', 'TCS.NS', 'TATAGLOBAL.BO', 'TATAMOTORS.BO', 'TATAPOWER.BO', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TECHM.BO', 'TECHM.NS', 'TITAN.BO', 'TITAN.NS', 'UCOBANK.NS', 'UNIONBANK.BO', 'UNIONBANK.NS', 'UNITECH.BO', 'UNITECH.NS', 'UPL.BO', 'VOLTAS.BO', 'VOLTAS.NS', 'YESBANK.BO', 'YESBANK.NS', 'ZEEL.NS', 'IOC.NS', 'IOC.BO', 'ICICIBANK.NS', 'ICICIBANK.BO', 'IDBI.BO', 'IDBI.NS', 'IDFC.NS', 'IDFC.BO', 'IFCI.BO', 'IFCI.NS', 'ITC.NS', 'ITC.BO', 'IDEA.NS', 'IDEA.BO', 'INDIACEM.NS', 'INDIACEM.BO', 'IBREALEST.NS', 'IBREALEST.BO', 'IOB.NS', 'IOB.BO', 'IGL.NS', 'IGL.BO', 'INDUSINDBK.BO', 'INFY.NS', 'INFY.BO']
# 
# def cutter(lis,which):
#     return lis[:which] + lis[which+1:]
# 
# kat = cutter(kat,16)
# kat = cutter(kat,19)
# kat = cutter(kat,23)
# kat = cutter(kat,23)
# kat = cutter(kat,26)
# kat = cutter(kat,28)
# kat = cutter(kat,31)
# kat = cutter(kat,42)
# kat = cutter(kat,43)
# kat = cutter(kat,50)
# kat = cutter(kat,51)
# kat = cutter(kat,56)
# kat = cutter(kat,62)
# kat = cutter(kat,67)
# kat = cutter(kat,78)
# kat = cutter(kat,79)
# kat = cutter(kat,80)
# kat = cutter(kat,90)
# kat = cutter(kat,101)
# kat = cutter(kat,110)
# kat = cutter(kat,110)
# kat = cutter(kat,113)
# kat = cutter(kat,119)
# kat = cutter(kat,123)
# kat = cutter(kat,138)
# kat = cutter(kat,146)
# kat = cutter(kat,147)
# 
# print kat
# print len(kat)
#===============================================================================

#===============================================================================
# final_kat = ['ARVIND.BO', 'ARVIND.NS', 'DISHTV.BO', 'DISHTV.NS', 'HINDZINC.BO', 'HINDZINC.NS', 'WIPRO.BO', 'WIPRO.NS', 'ACC.BO', 'ACC.NS', 'ALBK.NS', 'AMBUJACEM.NS', 'ANDHRABANK.BO', 'APOLLOTYRE.BO', 'ASHOKLEY.BO', 'ASHOKLEY.NS', 'AXISBANK.NS', 'BANKINDIA.NS', 'BATAINDIA.NS', 'BHEL.BO', 'BHEL.NS', 'BPCL.BO', 'BPCL.NS', 'BIOCON.NS', 'CESC.BO', 'CESC.NS', 'CAIRN.NS', 'CANBK.NS', 'CIPLA.BO', 'CIPLA.NS', 'COLPAL.NS', 'DLF.NS', 'DABUR.BO', 'DABUR.NS', 'DIVISLAB.BO', 'DIVISLAB.NS', 'DRREDDY.BO', 'DRREDDY.NS', 'EXIDEIND.BO', 'EXIDEIND.NS', 'GAIL.BO', 'GAIL.NS', 'GMRINFRA.NS', 'GODREJIND.NS', 'GRASIM.BO', 'GRASIM.NS', 'HCLTECH.BO', 'HCLTECH.NS', 'HDFCBANK.BO', 'HDFCBANK.NS', 'HAVELLS.NS', 'HEXAWARE.BO', 'HEXAWARE.NS', 'HINDALCO.BO', 'HINDALCO.NS', 'HINDPETRO.NS', 'HDIL.NS', 'HDFC.BO', 'HDFC.NS', 'JSWSTEEL.NS', 'JPPOWER.BO', 'JPPOWER.NS', 'KTKBANK.NS', 'KOTAKBANK.BO', 'KOTAKBANK.NS', 'LICHSGFIN.BO', 'LICHSGFIN.NS', 'MRF.NS', 'MARUTI.BO', 'MARUTI.NS', 'NMDC.NS', 'NTPC.BO', 'NTPC.NS', 'ONGC.BO', 'ONGC.NS', 'OFSS.NS', 'PTC.BO', 'PTC.NS', 'PETRONET.NS', 'PFC.NS', 'POWERGRID.NS', 'PNB.BO', 'PNB.NS', 'RANBAXY.BO', 'RANBAXY.NS', 'RCOM.BO', 'RCOM.NS', 'RELIANCE.NS', 'RELINFRA.BO', 'RELINFRA.NS', 'RPOWER.NS', 'RECLTD.BO', 'RECLTD.NS', 'SSLT.BO', 'SIEMENS.BO', 'SIEMENS.NS', 'SBIN.NS', 'SAIL.BO', 'SAIL.NS', 'SUNPHARMA.BO', 'SUNPHARMA.NS', 'SUNTV.NS', 'SYNDIBANK.BO', 'SYNDIBANK.NS', 'TATACHEM.BO', 'TATACHEM.NS', 'TATACOMM.BO', 'TATACOMM.NS', 'TCS.BO', 'TCS.NS', 'TATAPOWER.BO', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.BO', 'TITAN.NS', 'UCOBANK.NS', 'UNIONBANK.BO', 'UNIONBANK.NS', 'UNITECH.NS', 'UPL.BO', 'VOLTAS.BO', 'VOLTAS.NS', 'YESBANK.NS', 'ZEEL.NS', 'IOC.NS', 'IOC.BO', 'ICICIBANK.NS', 'ICICIBANK.BO', 'IDBI.BO', 'IDBI.NS', 'IDFC.NS', 'IDFC.BO', 'IFCI.BO', 'IFCI.NS', 'ITC.NS', 'ITC.BO', 'IDEA.NS', 'INDIACEM.NS', 'INDIACEM.BO', 'IBREALEST.NS', 'IBREALEST.BO', 'IOB.NS', 'IOB.BO', 'IGL.NS', 'IGL.BO', 'INFY.NS']
# for i in range( len(final_kat) ):
#     page = 'https://ichart.finance.yahoo.com/table.csv?s=' + final_kat[i] + '&d=4&e=26&f=2014&g=d&a=0&b=3&c=2000&ignore=.csv'
#     print i
#     opn=urllib2.urlopen(page)
#===============================================================================

#===============================================================================
# kate = ['ARVIND.BO', 'ARVIND.NS', 'DISHTV.BO', 'DISHTV.NS', 'HINDZINC.BO', 'HINDZINC.NS', 'WIPRO.BO', 'WIPRO.NS', 'ACC.BO', 'ACC.NS', 'ALBK.NS', 'AMBUJACEM.NS', 'ANDHRABANK.BO', 'APOLLOTYRE.BO', 'ASHOKLEY.BO', 'ASHOKLEY.NS', 'AXISBANK.NS', 'BANKINDIA.NS', 'BATAINDIA.NS', 'BHEL.BO', 'BHEL.NS', 'BPCL.BO', 'BPCL.NS', 'BIOCON.NS', 'CESC.BO', 'CESC.NS', 'CAIRN.NS', 'CANBK.NS', 'CIPLA.BO', 'CIPLA.NS', 'COLPAL.NS', 'DLF.NS', 'DABUR.BO', 'DABUR.NS', 'DIVISLAB.BO', 'DIVISLAB.NS', 'DRREDDY.BO', 'DRREDDY.NS', 'EXIDEIND.BO', 'EXIDEIND.NS', 'GAIL.BO', 'GAIL.NS', 'GMRINFRA.NS', 'GODREJIND.NS', 'GRASIM.BO', 'GRASIM.NS', 'HCLTECH.BO', 'HCLTECH.NS', 'HDFCBANK.BO', 'HDFCBANK.NS', 'HAVELLS.NS', 'HEXAWARE.BO', 'HEXAWARE.NS', 'HINDALCO.BO', 'HINDALCO.NS', 'HINDPETRO.NS', 'HDIL.NS', 'HDFC.BO', 'HDFC.NS', 'JSWSTEEL.NS', 'JPPOWER.BO', 'JPPOWER.NS', 'KTKBANK.NS', 'KOTAKBANK.BO', 'KOTAKBANK.NS', 'LICHSGFIN.BO', 'LICHSGFIN.NS', 'MRF.NS', 'MARUTI.BO', 'MARUTI.NS', 'NMDC.NS', 'NTPC.BO', 'NTPC.NS', 'ONGC.BO', 'ONGC.NS', 'OFSS.NS', 'PTC.BO', 'PTC.NS', 'PETRONET.NS', 'PFC.NS', 'POWERGRID.NS', 'PNB.BO', 'PNB.NS', 'RANBAXY.BO', 'RANBAXY.NS', 'RCOM.BO', 'RCOM.NS', 'RELIANCE.NS', 'RELINFRA.BO', 'RELINFRA.NS', 'RPOWER.NS', 'RECLTD.BO', 'RECLTD.NS', 'SSLT.BO', 'SIEMENS.BO', 'SIEMENS.NS', 'SBIN.NS', 'SAIL.BO', 'SAIL.NS', 'SUNPHARMA.BO', 'SUNPHARMA.NS', 'SUNTV.NS', 'SYNDIBANK.BO', 'SYNDIBANK.NS', 'TATACHEM.BO', 'TATACHEM.NS', 'TATACOMM.BO', 'TATACOMM.NS', 'TCS.BO', 'TCS.NS', 'TATAPOWER.BO', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.BO', 'TITAN.NS', 'UCOBANK.NS', 'UNIONBANK.BO', 'UNIONBANK.NS', 'UNITECH.NS', 'UPL.BO', 'VOLTAS.BO', 'VOLTAS.NS', 'YESBANK.NS', 'ZEEL.NS', 'IOC.NS', 'IOC.BO', 'ICICIBANK.NS', 'ICICIBANK.BO', 'IDBI.BO', 'IDBI.NS', 'IDFC.NS', 'IDFC.BO', 'IFCI.BO', 'IFCI.NS', 'ITC.NS', 'ITC.BO', 'IDEA.NS', 'INDIACEM.NS', 'INDIACEM.BO', 'IBREALEST.NS', 'IBREALEST.BO', 'IOB.NS', 'IOB.BO', 'IGL.NS', 'IGL.BO', 'INFY.NS']
# i=0
# while(kate[i]!='INFY.NS'):
#     if(kate[i][:-3]==kate[i+1][:-3]):
#         kate = (kate[:i+1] + kate[i+2:])
#     else:
#         i=i+1
# 
# print kate
#===============================================================================

#===============================================================================
# A=[1,2,3,4,5,6]
# print A[4:1]
#===============================================================================


#----------------------------------------------------- execfile("data_dload.py")
#--------------------------------------------------------------------- print kat

#---------------------------------------------------- os.system("data_dload.py")


#-------------------------------------------------- execfile("date_generate.py")

##################################################################################

def filler(lst):
    i = 0
    ctr=0
    while(i<len(lst)-1):
        if(lst[i]==0):
            mark1 = i-1
            i = i+1
            while(lst[i]==0):
                ctr = ctr+1
                i = i+1
            mark2 = i
            if(mark2==len(lst)):
                break
            for j in range(mark1+1,mark2):
                 lst[j] =   lst[mark1] +  (j-mark1)*(lst[mark2]-lst[mark1])/(mark2-mark1)
        i = i+1
    return lst
# print filler([10.53,0,0,0,5.467])
def inssort(this_list, that_elem):
    this_list
    if(this_list==[]):
        this_list.append(that_elem)
        return this_list
    elif(that_elem<=this_list[-1]):
        this_list.append(that_elem)
        return this_list
    else:
        x=inssort(this_list[:-1], that_elem)
        x.append(this_list[-1])
        return x

def sorter(act_list,switcheroo):
    lust=[]
    for i in range(len(act_list)):
        lust=inssort(lust,act_list[i])

    if(switcheroo==0):
        return lust

    ranker=range(len(act_list))
    for i in range(len(act_list)):
        for j in range(len(act_list)):
            if(lust[i]==act_list[j]):
                ranker[i]=j
                act_list[j]=lust[0]-1
                break
    else:
        return ranker

with open('yawho.csv','rb') as f:
    rdr=csv.reader(f)
    prek=[]
    for row in rdr:
        prek.append(row)
k=prek[2:]
i=0
while(k[i][0]!='INFY.NS'):
    if(k[i][0][:-3]==k[i+1][0][:-3]):
        k = k[:i+1] + k[i+2:]
    else:
        i=i+1
# print k[0][-10]
newk=numpy.zeros([len(k),len(k[0][2139:-10])])
for i in range(len(k)):
    for j in range(len(k[0][2139:-10])):
        newk[i][j]=float(k[i][j+2139])

Matt = newk.copy()
for i in range(len(newk)):
    filler(Matt[i])

for i in range(len(Matt)):
    Matt[i] = Matt[i] - numpy.mean(Matt[i])


cormtx=numpy.corrcoef(Matt)
abscormtx=numpy.abs(cormtx)


for i in range(len(abscormtx)):
    abscormtx[i][i] = abscormtx[i][i] - numpy.sum(abscormtx[i])
#--------------------------------------------------- print lin.eig(abscormtx)[0]
#------------------------------------------------------------------------------ 
#--------------- plot(range(len(abscormtx)),sorter(lin.eig(abscormtx)[0],0),'o')
#------------------------------------------------------------------------ show()
################################################################################
X = numpy.zeros([6,6])
X[0] = [1,0,0,0,0,0]
X[1] = [1.1,0,0.1,0,0,0]
X[2] = [0,0,1,0,0,0]
X[3] = [0,0.1,1.1,0,0.1,0]
X[4] = [0,0,0,0,0,1]
X[5] = [0,0.1,0.1,0,0,1]

db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples = db.core_sample_indices_
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print n_clusters_


centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4, random_state=0)
X = StandardScaler().fit_transform(X)
print X

