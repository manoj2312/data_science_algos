'''
Created on Jul 11, 2014

@author: admin
'''
import csv
from numpy import corrcoef
import numpy
#===============================================================================
# import statsmodels
# from statsmodels.tsa.stattools import adfuller
#===============================================================================
from matplotlib.pylab import plot
from matplotlib.pylab import show
from sklearn.decomposition import PCA
from sklearn.cluster import spectral_clustering
from z_func import filler
from z_func import bestcomp

# The following block is used to read data from the csv file. Read data is stored in 'newk'.
# 'filler'-function is implemented on 'Matt-a copied version of 'newk'. 'filler' averages data around holidays to obtain a continuous series of values that are analyzable.
# Modifications are done to shift all stocks' prices to mean-center around 0.
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
#===============================================================================
# # sample to show the difference before and after 'filler' is used.
# plot(range(len(newk[25])),newk[25])
# plot(range(len(Matt[25])),Matt[25])
# show()
#===============================================================================

# print len(Matt) # == 93    

# PCA is performed on total data available. (i.e. entire timeline)
# The stock in whose direction maximum variance persists is determined. 'bestcomp' is called for this purpose.
pca=PCA(n_components=93)
pca.fit(Matt.T)
Zo = pca.components_
print 'the most dominant component is ' + k[bestcomp(Zo)][0] + ' index: ' + str(bestcomp(Zo)) + '\nthe PCs mag. in its direction is ' + str(Zo[0][bestcomp(Zo)])
num=bestcomp(Zo)


# # Slope test- A statistical test which examines the significance of the linearity of the relation predicted by PCA. We need a dependent stock and a depend-on stock. We take the bestcomp stock as our dependent stock and the stock whose significance to be determined as depend-on stock.
# # 'MRFarr' is the list of actual values of the bestcomp-stock. 'expMRF' is the list of expected values based on the PCA coefficients derived from the n-1 dimensional hyperplane of maximum variance.
# # 'ymean' is calculated to further be incorporated in the calculation of Standard Error.
#----- # SE = sqrt [ sigma(yi - Yi)^2 / (n - k - 1) ] / sqrt [ sigma(xi - x)^2 ]
#-------------------------------------------------------------- MRFarr=Matt[num]
#----------------------------------------------- expMRF=numpy.zeros(len(MRFarr))
#------------------------------------------------- for rain in range(len(Matt)):
    #------------------------------------------------------------ if(rain!=num):
        #------------------------------- expMRF=expMRF-(Zo[-1][rain]*Matt[rain])
#----------------------------------------------------- expMRF=expMRF/Zo[-1][num]
#------------------------------------------------------------------------------ 
# plot(range(len(MRFarr)),MRFarr,'g')                        #checked the goodness of approximation of MRF, by the rest of the stocks as PCs using PCA
#------------------------------------------- plot(range(len(MRFarr)),expMRF,'.')
#------------------------------------------------------------------------ show()
#------------------------------------------------------------------------------ 
#------------------------------------------------------------ yarr=MRFarr-expMRF
#-------- ymean=numpy.sqrt((numpy.mean(yarr*yarr))/ (len(Matt[0])-len(Matt)-1) )



# deciding number of clusters
iterval=20
plotter = numpy.zeros(iterval)
plotter1 = numpy.zeros(iterval)

# 'abscormtx' is the correlation matrix of all stocks with all values made absolute as our concern is the magnitude and not the sign. 
cormtx=corrcoef(Matt)   
abscormtx=numpy.abs(cormtx)

holdon = []

# The following 'for' loop finds value for designed statistic for different initializations of clusters and chooses the best number of clusters.
# Optimizer statistic = mean(variance of correlations within clusters)/mean(variance of cross-correlations over clusters) . -> minimize this statistic for optimal number of clusters.

for no_clusters in numpy.arange(2,len(plotter)+2):
    binall =  spectral_clustering(abscormtx,no_clusters)
   
# 'septa' is the clustered list with names of stocks.
# 'numblist' is the clustered list with indices of stocks.
    septa=[]
    numblist=[]
    for i in range(no_clusters):
        septa.append([])
        numblist.append([])    
    for i in range(len(binall)):
        septa[binall[i]].append(newk[i][0])
        numblist[binall[i]].append(i)
    
    holdon.append(numblist)
    
# 'cluster_var' is the list of variances of correlations within clusters
    cluster_var=numpy.zeros(no_clusters)
    for i in range(no_clusters):
        temparr=numpy.zeros([len(numblist[i]),len(Matt[0])])
        for krain in range(len(numblist[i])):
            temparr[krain]=Matt[numblist[i][krain]]
        tempcorr=corrcoef(temparr)    
        tempcorr=numpy.abs(tempcorr)       
        cluster_var[i]=numpy.var(tempcorr)
        
    mean_cluster_var=numpy.mean(cluster_var)
    sum_cluster_var=numpy.sum(cluster_var)
    
# 'paired_var' is the matrix of variances of cross-correlations over clusters
    paired_var=numpy.zeros([no_clusters,no_clusters])
    for i in range(no_clusters):
        for j in range(no_clusters):
            if(i!=j):
                tempjoin=[]
                tempjoin.extend(numblist[i])
                tempjoin.extend(numblist[j])
                
                temparr=numpy.zeros([len(tempjoin),len(Matt[0])])
                for krain in range(len(tempjoin)):
                    temparr[krain]=Matt[tempjoin[krain]]

                tempcorr=corrcoef(temparr)    
                tempcorr=numpy.abs(tempcorr)
            
                paired_var[i][j]=numpy.var( tempcorr[ :len(numblist[i]) , len(numblist[i]):len(tempjoin) ] )
            
    
    mean_paired_var=(numpy.sum(paired_var))/((no_clusters)*(no_clusters-1))
    sum_paired_var=numpy.sum(paired_var)
    
    plotter[no_clusters-2] = mean_cluster_var/mean_paired_var
#     plotter1[no_clusters-2] = sum_cluster_var/sum_paired_var


for i in range(iterval):
    if(plotter[i]==min(plotter)):
        no_clusters=i+2
        break 

print 'number of clusters determined is ' + str(no_clusters)

# plotting the value of Optimizer statistic for different number of clusters.
plot(range(2,len(plotter)+2),plotter)
show()

numlist = holdon[i]

print numlist
# # Writes all data obtained into a file in csv format. First the indices of stocks of each cluster are written. Then the correlation matrix of each cluster is written.
#------------------------------------ file_open = open('corrmatrixall.csv', 'w')
#------------------------------------------------------------------------------ 
#-------------------------------------------------- for i in range(no_clusters):
    #------------------------------------------ for j in range(len(numlist[i])):
        #--------------------------- file_open.write( str(numlist[i][j]) + ',' )
    #----------------------------------------------------- file_open.write('\n')
#------------------------------------------------------------------------------ 
#--------------------------------------------------------- file_open.write('\n')
#-------------------------------------------------- for i in range(no_clusters):
    #---------------------- helpcorr=numpy.zeros([len(numlist[i]),len(Matt[0])])
    #-------------------------------------- for krain in range(len(numlist[i])):
        #------------------------------- helpcorr[krain]=Matt[numlist[i][krain]]
    #----------------------------------------------- helpcorr=corrcoef(helpcorr)
    #---------------------------------------------- helpcorr=numpy.abs(helpcorr)
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
    #-------------------------------------------- for p in range(len(helpcorr)):
        #----------------------- file_open.write(newk[ numlist[i][p] ][0] + ',')
    #----------------------------------------------------- file_open.write('\n')
#------------------------------------------------------------------------------ 
    #-------------------------------------------- for l in range(len(helpcorr)):
        #------------------------------------- for m in range(len(helpcorr[0])):
            #------------------------ file_open.write(str(helpcorr[l][m]) + ',')
        #------------------------------------------------- file_open.write('\n')
#------------------------------------------------------------------------------ 
    #--------------------------------------------------- file_open.write('\n\n')
#------------------------------------------------------------------------------ 
#------------------------------------------------------------- file_open.close()
