import csv
import sklearn
import string
import numpy
from scipy import stats
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
  
  
  
for i in range(1,119):
    for j in range(1,1024):
        k[i][j]=float(k[i][j])
          
 
newk=k[1: ]
 
 
Matt=numpy.zeros([118,1023])
 
for j in range(118):
    Matt[j]=newk[j][1:]-numpy.mean(newk[j][1:])
     
      
cormtx=corrcoef(Matt)   
abscormtx=numpy.abs(cormtx)
 
no_clusters = 4
 
# binall =  spectral_clustering(abscormtx,no_clusters)
#     
# septa=[]
# numlist=[]
# 
# for i in range(no_clusters):
#     septa.append([])
#     numlist.append([])
#         
# for i in range(len(binall)):
#     septa[binall[i]].append(Matt[i][0])
#     numlist[binall[i]].append(i)
 
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
     
  
########################
 
numer=numpy.array([0,0,0,0])
 
for j in range(no_clusters):
    for i in range(len(Zoer[j][0])):
        if(Zoer[j][0][i]==max(Zoer[j][0])):
            numer[j]=i
 
 
MRFarr=numpy.zeros([no_clusters,1023])
 
for i in range(no_clusters):
     
    #print newk[numlist[i][numer[i]]][0]
     
    MRFarr[i] = Matter[i][numer[i]]
    
 
expMRF=numpy.zeros([no_clusters,1023])
 
for i in range(no_clusters):
    for rain in range(len(Matter[i])):
        if(rain!=numer[i]):
            expMRF[i]=expMRF[i]-(Zoer[i][len(Zoer[i])-1][rain]*Matter[i][rain])
    expMRF[i]=expMRF[i]/Zoer[i][len(Zoer[i])-1][numer[i]]
    
    
 
# plot(range(1023),MRFarr[0],'g')                        #checked the goodness of approximation of MRF, by the rest of the stocks as PCs using PCA
# plot(range(1023),expMRF[0],'b')
# show()
# 
# plot(range(1023),MRFarr[1],'g')                        #checked the goodness of approximation of MRF, by the rest of the stocks as PCs using PCA
# plot(range(1023),expMRF[1],'b')
# show()
# 
# plot(range(1023),MRFarr[2],'g')                        #checked the goodness of approximation of MRF, by the rest of the stocks as PCs using PCA
# plot(range(1023),expMRF[2],'b')
# show()
# 
# plot(range(1023),MRFarr[3],'g')                        #checked the goodness of approximation of MRF, by the rest of the stocks as PCs using PCA
# plot(range(1023),expMRF[3],'b')
# show()
   
 
yarr=MRFarr-expMRF
 
ymean=numpy.zeros(no_clusters)
 
for i in range(no_clusters):
    ymean[i]=numpy.sqrt((numpy.mean(yarr[i]*yarr[i]))/904)
      
def SE(rain,i):
    if(rain==numer[i]):
        return Zoer[i][len(Zoer[i])-1][rain]
    xmean=numpy.mean(Matter[i][rain]*Matter[i][rain])
    return ymean[i]/(numpy.sqrt(xmean))
   
   
   
binchk=numpy.zeros(118)
 
 
def stkfltr(sgval,i):
    rainchk=[]
    leftout=[]
    for rainer in range(len(Zoer[i])):
        tt=Zoer[i][len(Zoer[i])-1][rainer]/SE(rainer,i)
        tt=(-tt)/Zoer[i][len(Zoer[i])-1][numer[i]]
        pval = (stats.t.sf(numpy.abs(tt), 1022-len(Matter[i])))*2
        if(pval>=sgval):
            rainchk.append(rainer)
#             binchk[rainer]=binchk[rainer]+1
#             if(binchk[rainer]==1):
#                 print newk[rainer][0]
        else:
            leftout.append(rainer)
     
    return rainchk
      
def stkr(sgval,i):                                      #Since the P-value (0.0242) is less than the significance level (0.05), there is significant linear relation
    rainchk=[]
    leftout=[]
    for rainer in range(len(Zoer[i])):
        tt=Zoer[i][len(Zoer[i])-1][rainer]/SE(rainer,i)
        tt=(-tt)/Zoer[i][len(Zoer[i])-1][numer[i]]
        pval = (stats.t.sf(numpy.abs(tt), 1022-len(Matter[i])))*2
        if(pval>=sgval):
            rainchk.append(rainer)
        else:
            leftout.append(rainer)
             
#     if(len(leftout)==8):
#         for j in range(len(leftout)):
#             print newk[numlist[i][leftout[j]]][0]
#         return 1
#     if(len(rainchk)==6):
#         for j in range(len(rainchk)):
#             print newk[numlist[i][rainchk[j]]][0]
#         return 1
 
    return 0
 
# sgval=0.99
# Listed=stkfltr(sgval)
# print len(Listed) 
# for rin in range(len(stkfltr(sgval))):
#     print newk[Listed[rin]][0]      
 
 
 
for i in range(no_clusters):
    xaxis=numpy.logspace(-5,0,1000)
    yaxis=numpy.zeros(len(xaxis))
           
        
        
    for runner in range(len(xaxis)):
        yaxis[runner]=len(stkfltr(1-(xaxis[runner]),i))
 
    for runner in range(len(xaxis)):
        if(stkr(1-(xaxis[runner]),i)==1):
            break
 
 
    plot(xaxis,yaxis,'.')
    show()

        