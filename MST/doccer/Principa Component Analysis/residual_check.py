'''
Created on Jun 10, 2014

@author: admin
'''
import csv
import sklearn
import string
import numpy
import scipy
from scipy import stats
import statsmodels
from statsmodels.tsa.stattools import adfuller 
from matplotlib.pylab import plot
from matplotlib.pylab import show
from sklearn.decomposition import PCA
from sklearn.cluster import spectral_clustering
from numpy import corrcoef
 

with open('Mean_Reversion_strategy_data_PRICES.csv','rb') as f:
    rdr=csv.reader(f)
    k=[]
    for row in rdr:
        k.append(row)
  

  
for i in range(1,len(k)):
    for j in range(1,len(k[0])):
        k[i][j]=float(k[i][j])
          
 
newk=k[1: ]
 
 
Matt=numpy.zeros([118,1023])
 
for j in range(118):
    Matt[j]=newk[j][1:]-numpy.mean(newk[j][1:])
     
      
cormtx=corrcoef(Matt)   
abscormtx=numpy.abs(cormtx)
 
no_clusters = 4                                             #retrieve from variance_test
  
with open('corrmatrixall.csv','rb') as f:
    rdr=csv.reader(f)
    numlist=[]
    i=0
    for row in rdr:
        if(i<4):
            numlist.append(row)
        else:
            break
        i=i+1
         
for i in range(len(numlist)):
    for j in range(len(numlist[i])):
        if(numlist[i][j]==''):
            numlist[i]=numlist[i][:j]
            break
        else:
            numlist[i][j] = int(numlist[i][j])
 
 
         
Matter=[]
 
for i in range(no_clusters):
    Matter.append( Matt[numlist[i]] )
 
 
Zoer=[]
 
for i in range(no_clusters):
    pca = PCA(n_components=len(Matter[i]))
    pca.fit(Matter[i].T)
    Zoer.append(pca.components_)
     

slash=[72, 33, 56, 44, 19, 9, 13, 104, 1, 69, 43, 57, 82, 5, 37, 42, 16, 87, 70, 11, 102, 116, 62, 30, 108, 0, 49, 35, 73, 45, 34, 40, 71, 51, 110, 22, 46, 23, 26, 101, 97, 2]
# slash=[63, 12, 47, 4, 10, 27, 52, 20, 60, 61, 91, 99, 15, 80, 94, 115, 53, 86, 8, 106, 48, 17, 31, 6, 98, 95, 3, 67, 18, 100, 93, 85, 38, 14, 24, 64, 111, 36, 109]
# slash=[89, 112, 105, 66, 55, 39, 59, 77, 76, 90, 88, 50, 113, 21, 25, 32, 92, 65, 58, 81, 83, 96]
# slash=[79, 84, 54, 28, 41, 103, 74, 68, 114, 107, 78, 29, 7, 117, 75]
storeth=[]
for i in range(len(Zoer[0])-2):
    res=numpy.zeros(1023)
    slashet=slash[:3+i]
    pca=PCA(n_components=len(slashet))  
    shet=numpy.zeros([2+i,1023])
    for rain in range(len(shet)):
        shet[rain]=Matt[rain]
    pca.fit(shet.T)
    storeth.append(pca.components_[-1])
    for j in range(1023):
        for ij in range(len(storeth[-1])):
            res[j]=res[j]+storeth[-1][ij]*shet[ij][j]
#     print numpy.mean(res)
    
    print adfuller(res, maxlag=None, regression='c', autolag='AIC', store=False, regresults=False)[0]

