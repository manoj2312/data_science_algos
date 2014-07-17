'''
Created on Jun 2, 2014

@author: admin
'''
import array
import csv
import numpy
from numpy import corrcoef
from numpy.linalg import det
import scipy
from scipy import stats
from matplotlib.pylab import plot
from matplotlib.pylab import show
import sklearn
from sklearn.decomposition import PCA
from sklearn.cluster import spectral_clustering



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
    
     
Matt=Matt[ : , :512]

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
    
ymean=numpy.sqrt((numpy.mean(yarr*yarr))/ (len(Matt)) )
    
def SE(rain):
    xmean=numpy.mean(Matt[rain]*Matt[rain])
    return ymean/(numpy.sqrt(xmean))
 
 
 
binchk=numpy.zeros(118)
    
def stkfltr(sgval):
    rainchk=[]
    leftout=[]
    for rainer in range(118):
        tt=Zo[117][rainer]/SE(rainer)
        pval = (stats.t.sf(numpy.abs(tt), (len(Matt[0])-118-1) ))*2
        
        if(pval>=sgval):
            rainchk.append(rainer)
#             binchk[rainer]=binchk[rainer]+1
#             if(binchk[rainer]==1):
#                 print newk[rainer][0]
        else:
            leftout.append(rainer)
    return leftout
    

sgval=1
Listed=stkfltr(sgval)
print len(Listed)
Names=[] 
for rin in range(len(stkfltr(sgval))):
    Names.append(newk[Listed[rin]][0])
#     print Names[rin]      
     
  
arrformx=numpy.zeros([len(Listed), (len(Matt[0])) ])
for krain in range(len(Listed)):
    arrformx[krain]=Matt[Listed[krain]]
     
cormtx=corrcoef(arrformx)   
abscormtx=numpy.abs(cormtx)

# file_open = open('corrmatrixall.csv', 'a')    
#    
# for p in range(len(cormtx)):
#     file_open.write(newk[Listed[p]][0] + ',')
#  
# file_open.write('\n')
#      
# for l in range(len(cormtx)):
#     for m in range(len(cormtx[0])):
#         file_open.write(str(cormtx[l][m]) + ',')
#     file_open.write('\n')
#     
# file_open.write('\n\n')
#           
# file_open.close()



iterval=4
plotter = numpy.zeros(iterval)
plotter1 = numpy.zeros(iterval)
plotter2 = numpy.zeros(iterval)

totalcorr=corrcoef(Matt)
# totalsum=numpy.sum(totalcorr)

####
for no_clusters in numpy.arange(2,len(plotter)+2):
    
    binall =  spectral_clustering(abscormtx,no_clusters)
    if(no_clusters==5):
        print binall
    
    septa=[]
    numlist=[]
    for i in range(no_clusters):
        septa.append([])
        numlist.append([])
    
    for i in range(len(binall)):
        septa[binall[i]].append(Names[i])
        numlist[binall[i]].append(Listed[i])
    
    

    resepta=[]
    for i in range(no_clusters):
        resepta.extend(numlist[i])
    
        

#     s=numpy.zeros(no_clusters)
#     denom=totalsum
#     num=0
    
    
    
    
    
    for i in range(no_clusters):
        temparr=numpy.zeros([len(numlist[i]),len(Matt[0])])
        for krain in range(len(numlist[i])):
            temparr[krain]=Matt[numlist[i][krain]]
        tempcorr=corrcoef(temparr)    
        tempcorr=numpy.abs(tempcorr)
        
#         s[i]=numpy.mean(tempcorr)
#         denom=denom-numpy.sum(tempcorr)
#         num=num+numpy.sum(tempcorr)
        
        
        
        
        
#     someconst=float(118**2)
#     for i in range(no_clusters):
#         someconst=someconst-(len(septa[i]))**2
# #         if(no_clusters==5):
# #             print len(septa[i])

    
#     num=num/((118**2)-someconst)    
#     denom=denom/someconst
    
    
    plotter[no_clusters-2] = num#(2*numpy.mean(s))/denom
    plotter1[no_clusters-2] = 1/denom
#     plotter2[no_clusters-2] = 


# plot(range(len(plotter)),plotter)
# show()
# plot(range(len(plotter1)),plotter1)
# show()
# plot(range(len(plotter2)),plotter2)
# show()

# file_open = open('corrmatrixall.csv', 'a')
#  
# file_open.write('\n\n')    
#   
# for p in range(len(resepta)):
#     file_open.write(newk[resepta[p]][0] + ',')
# 
# file_open.write('\n')
#     
# for l in range(len(abscormtx_1)):
#     for m in range(len(abscormtx_1[0])):
#         file_open.write(str(abscormtx_1[l][m]) + ',')
#     file_open.write('\n')
#          
# file_open.close()

