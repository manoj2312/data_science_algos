'''
Created on Jun 2, 2014

@author: admin
'''
import csv
import sklearn
import string
import numpy
from scipy import stats
import matplotlib.pylab
from sklearn.decomposition import PCA
from numpy import corrcoef

with open('Mean_Reversion_strategy_data_PRICES.csv','rb') as f:
    rdr=csv.reader(f)
    k=[]
    for row in rdr:
        k.append(row)
 
 
 
for i in range(1,119):
    for j in range(1,1024):
        k[i][j]=float(k[i][j])
         

newk=k[1: ]


Matt=numpy.zeros([118,1023])

for j in range(118):
    Matt[j]=newk[j][1:]-numpy.mean(newk[j][1:])
    
     
pca=PCA(n_components=118)
pca.fit(Matt.T)

Zo = pca.components_

    

  
################################################################3
num=72
  
MRFarr=Matt[num]
  
expMRF=numpy.zeros(len(MRFarr))
for rain in range(118):
    if(rain!=num):
        expMRF=expMRF-(Zo[117][rain]*Matt[rain])
expMRF=expMRF/Zo[117][num]
  
  
  
# matplotlib.pylab.plot(range(1023),MRFarr,'g')                        #checked the goodness of approximation of MRF, by the rest of the stocks as PCs using PCA
# matplotlib.pylab.plot(range(1023),expMRF,'b')
# matplotlib.pylab.show()
 
yarr=MRFarr-expMRF
   
ymean=numpy.sqrt((numpy.mean(yarr*yarr))/904)
   
def SE(rain):
    if(rain==72):
        return Zo[117][rain]
    xmean=numpy.mean(Matt[rain]*Matt[rain])
    return ymean/(numpy.sqrt(xmean))



binchk=numpy.zeros(118)
   
def stkfltr(sgval):
    rainchk=[]
    leftout=[]
    for rainer in range(118):
        tt=Zo[117][rainer]/SE(rainer)
        pval = (stats.t.sf(numpy.abs(tt), 904))*2
        if(pval>=sgval):
            rainchk.append(rainer)
#             binchk[rainer]=binchk[rainer]+1
#             if(binchk[rainer]==1):
#                 print newk[rainer][0]
        else:
            leftout.append(rainer)
    return leftout
   

def stkr(sgval):                                      #Since the P-value (0.0242) is less than the significance level (0.05), there is significant linear relation
    rainchk=[]
    leftout=[]
    for rainer in range(len(Zo)):
        tt=Zo[len(Zo)-1][rainer]/SE(rainer)
        pval = (stats.t.sf(numpy.abs(tt), 1022-len(Matt)))*2
        if(pval>=sgval):
            rainchk.append(rainer)
        else:
            leftout.append(rainer)
            
    if(len(leftout)==8):
        for j in range(len(leftout)):  
            print newk[leftout[j]][0]
#             print Zo[len(Zo)-1][leftout[j]]/SE(leftout[j])
        return 1
#     if(len(rainchk)==8):
#         for j in range(len(rainchk)):
#             print newk[rainchk[j]][0]
# #             print Zo[len(Zo)-1][rainchk[j]]/SE(rainchk[j])
#         return 1

    return 0


xaxis=numpy.logspace(0,-5,1000)
yaxis=numpy.zeros(len(xaxis))


for runner in range(len(xaxis)):
    if(stkr(1-(xaxis[runner]))==1):
        break


# # sgval=0.99
# # Listed=stkfltr(sgval)
# # print len(Listed) 
# # for rin in range(len(stkfltr(sgval))):
# #     print newk[Listed[rin]][0]      
#     
#  
# arrformx=numpy.zeros([len(Listed),1023])
# for krain in range(len(Listed)):
#     arrformx[krain]=Matt[Listed[krain]]
#     
# cormtx=corrcoef(arrformx)   
#  
# print cormtx
#     
#     
# # file_open = open('corrmatrix.csv', 'a')     
# # for p in range(len(Listed)):
# #     file_open.write(newk[Listed[p]][0] + ',')
# #         
# # file_open.write('\n')
# #    
# # for l in range(len(cormtx)):
# #     for m in range(len(cormtx[0])):
# #         file_open.write(str(cormtx[l][m]) + ',')
# #     file_open.write('\n')
# #         
# # file_open.close()
#     
# # xaxis=numpy.logspace(0,-5,1000)
# # yaxis=numpy.zeros(len(xaxis))
# #          
# #       
# #       
# # for runner in range(len(xaxis)):
# #     yaxis[runner]=len(stkfltr(1-xaxis[runner]))
# #              
# #         
# #         
# # matplotlib.pylab.plot(xaxis,yaxis,'.')
# # matplotlib.pylab.show()
