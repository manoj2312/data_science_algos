'''
Created on Jun 19, 2014

@author: admin
'''

import numpy
from z_func import sorter
from z_func import stkfltr
import matplotlib
from matplotlib.pylab import plot
from matplotlib.pylab import show 

execfile("z_3_1_clustering.py")


#--------- # optional reading from the csv file instead of executing sub-program
#------------------------------------- with open('corrmatrixall.csv','rb') as f:
    #--------------------------------------------------------- rdr=csv.reader(f)
    #---------------------------------------------------------------- numlist=[]
    #----------------------------------------------------------------------- i=0
    #----------------------------------------------------------- for row in rdr:
        #-------------------------------------------------------------- if(i<4):
            #----------------------------------------------- numlist.append(row)
        #----------------------------------------------------------------- else:
            #------------------------------------------------------------- break
        #----------------------------------------------------------------- i=i+1
#------------------------------------------------------------------------------ 
#------------------------------------------------- for i in range(len(numlist)):
    #------------------------------------------ for j in range(len(numlist[i])):
        #------------------------------------------------ if(numlist[i][j]==''):
            #----------------------------------------- numlist[i]=numlist[i][:j]
            #------------------------------------------------------------- break
        #----------------------------------------------------------------- else:
            #-------------------------------- numlist[i][j] = int(numlist[i][j])

# the following code sorts the obtained clusters in the order of increasing size
numsort=numpy.zeros(len(numlist))
for i in range(len(numlist)):
    numsort[i]=len(numlist[i])

ranked = sorter(numsort,1)

new_numlist = []
for i in range(no_clusters):
    new_numlist.append( numlist[ranked[i]] )


# 'Matter' forms clusters and stores prices-data corresponding to the stocks of the cluster. 
Matter=[]
for i in range(no_clusters):
    Matter.append( Matt[new_numlist[i]] )

# 'Zoer' stores PCA model coefficients for every cluster that was stored using Matter.
Zoer=[]
for i in range(no_clusters):
    pca = PCA(n_components=len(Matter[i]))
    pca.fit(Matter[i].T)
    Zoer.append(pca.components_)
 
 
########################

# 'numer' stores the bestcomp-s of all clusters.  
#'MRFarr' is the set of all actual price values of all the bestcomp-s of the clusters.
# 'expMRF' is the set of all expected price values using the respective PCA models of all the bestcomp-s of the clusters.
numer=[]
for i in range(no_clusters):
    numer.append(0)
numer = numpy.array(numer)
for j in range(no_clusters):
    numer[j]=bestcomp(Zoer[j])

MRFarr=numpy.zeros([no_clusters,len(Matt[0])])
for i in range(no_clusters):
    #print newk[new_numlist[i][numer[i]]][0]
    MRFarr[i] = Matter[i][numer[i]]
expMRF=numpy.zeros([no_clusters,len(Matt[0])])
for i in range(no_clusters):
    for rain in range(len(Matter[i])):
        if(rain!=numer[i]):
            expMRF[i]=expMRF[i]-(Zoer[i][len(Zoer[i])-1][rain]*Matter[i][rain])
    expMRF[i]=expMRF[i]/Zoer[i][len(Zoer[i])-1][numer[i]]

# 'stkfltr' returns the list of the stocks' t-test statistics. 'tt_main' stores all these values for all clusters.
# We discard the least important stocks of each cluster as according to their t-test statistic.
# 'sorter' sorts each cluster into their descending order of importance as indicated by the t-test statistic.

tt_main=[]
for i in range(no_clusters):
    tt_main.append( stkfltr(numpy.random.rand(),Matter[i]) )

tember_numlist = []
for i in range(no_clusters):
    temb=[]
    L=sorter(tt_main[i],1)
    for j in L:
#         print newk[new_numlist[i][j]][0]
        temb.append(new_numlist[i][j])
    tember_numlist.append(temb)

print tember_numlist

#===============================================================================
# tember_namelist = tember_numlist
# for i in range(len(tember_numlist)):
#     print tember_numlist[i][0]
#     for j in range(len(tember_numlist[i])):
#         tember_namelist[i][j] = k[tember_namelist[i][j]][0]    
# 
# print tember_namelist
#===============================================================================

# optional plotting of most-contributing stock predicted vs actual. Helps determine the order of the residual signal with respect to the stock. Even if the residual is stationary, when it's magnitude increases, it hinders the PCA modeling process.
#-------------------------------------------------- for i in range(no_clusters):
    #--------------------------------- plot(range(len(MRFarr[i])),MRFarr[i],'g')
    #--------------------------------- plot(range(len(MRFarr[i])),expMRF[i],'b')
    #------------------------------------------ matplotlib.pylab.title(str(i+1))
    #-------------------------------------------------------------------- show()

file_open = open('clusstore.csv','w')
for i in range(len(tember_numlist)):
    print tember_numlist[i]
    for j in range(len(tember_numlist[i])):
        file_open.write( str(tember_numlist[i][j]) )
        if(j!=len(tember_numlist[i])-1):
            file_open.write(',')
        else:
            file_open.write('\n')

