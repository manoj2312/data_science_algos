'''
Created on Jun 24, 2014

@author: admin
'''
import array
import csv
import numpy
from numpy import corrcoef
from numpy.linalg import det
from numpy import dot
import scipy
from scipy import stats
import matplotlib
#===============================================================================
# import statsmodels
# from statsmodels.tsa.stattools import adfuller
#===============================================================================
from matplotlib.pylab import plot
from matplotlib.pylab import show
import sklearn
from sklearn.decomposition import PCA
from sklearn.cluster import spectral_clustering
from z_func import filler
from z_func import cutter


# 'clusunsun' represents which cluster among the clusters of 'clus' we want to trade on.
# 'dura' is the look-back period to calculate the SMA and Bollinger Bands.
# 'sart' represents the start point of the set of points on which you want to train your fixed PCA.
# 'endt' represents the end point of the set of points on which you want to train your fixed PCA.
clusunsun=3
dura = 15
sart = 500
endt = 800


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


#===============================================================================
# leftout = [1, 10, 17, 25, 50, 62, 66, 68, 74, 82, 91]
# for i in range(1,len(leftout)+1):
#     k = cutter(k,leftout[-i])
# 
# clus = []
# clus.append([8, 35, 52, 62, 11, 57, 33, 38, 42, 27, 45, 51, 36, 53, 65, 58, 1, 75, 43]) #-6
# clus.append([69, 63, 56, 34, 60, 13, 22, 49, 30])
# clus.append([6, 4, 73, 15, 66, 80, 48, 31, 12, 9, 20])
# clus.append([67, 79, 23, 32, 50, 55, 41, 68, 18, 78])   #-4.3
# clus.append([74, 36, 14, 37, 34, 51, 46, 69, 2])    #-4.3
# clus.append([71, 39, 0, 61, 77, 64, 26])    #-4.2
#===============================================================================


# conversion of all values in yawho.csv to float and then written into Matt.
# filler changes all holiday price values from 0 to a value which will fit linearly with the end values on either side
# All stocks in Matt are then mean-centered
newk=numpy.zeros([len(k),len(k[0][2139:-10])])
for i in range(len(k)):
    for j in range(len(k[0][2139:-10])):
        newk[i][j]=float(k[i][j+2139])
Matt = newk.copy()
for i in range(len(newk)):
    filler(Matt[i]) 
for i in range(len(Matt)):
    Matt[i] = Matt[i] - numpy.mean(Matt[i])


# Reading all clusters' constituents which were stored in 'clusstore.csv' after running z_3 into 'clus'
with open('clusstore.csv','rb') as f1:
    clus = []
    rdr=csv.reader(f1)
    for row in rdr:
        for i in range(len(row)):
            row[i] = int(row[i])
        clus.append(row)



# All initialisations. res is the dynamic PCA residual; res1 is the fixed PCA residual 
storeth=[]
compnum = 1
res=numpy.zeros(len(Matt[0]))
res1=numpy.zeros(len(Matt[0]))


# start of 'the' loop
# 'slashet' is the list of indices of the i-th cluster; 'shet' is the data corresponding to 'slashet', a subset of 'Matt' (Matt[slashet]); 'store' is the list containing the PC coefficients for maximum variability hyperpalne for 'trainval' number of data points of each stock.  
# 'storeth' is a list of sets of PC coefficients of the data which is assumed to be added dynamically at every t.
#stknum is a product of the loop. It consists of rectified dynamic PC coefficients.
stknum=[]
slashet=clus[clusunsun]
shet=Matt[slashet]

# fixed PCA model; res1(t) = store[0]*price_of_stock0(t) + store[1]*price_of_stock1(t) + store[2]*price_of_stock2(t) + .....
pca=PCA(n_components=len(slashet))
pca.fit(shet[:,sart:endt].T)
store = pca.components_[compnum-1-1]
for j in range(len(shet[0])):
    res1[j] = dot(store,shet.T[j].T)

# dynamic PCA model; res(t) = tmpor(t)[0]*price_of_stock0(t) + tmpor(t)[1]*price_of_stock1(t) + tmpor(t)[2]*price_of_stock2(t) + .....
for j in range(len(shet[0])):
    if(j<sart):
        tmpor = numpy.zeros(len(clus[clusunsun]))
    else:
        pca=PCA(n_components=len(slashet))
        pca.fit(shet[:,sart:j+1].T)
        tmpor = pca.components_[-1]
        if(numpy.dot(tmpor,store)<0):
            tmpor = -tmpor
        res[j] = dot(tmpor,shet.T[j].T)
    stknum.append(tmpor)

print 'fixed PC coefficients:\n' + str(store)

plot(range(len(res)),res,'r')
plot(range(len(res)),res1,'g')
# matplotlib.pylab.ylim(-50,50)
show()

# plots correlation for res and res1 using the first 'i' points.
corre = numpy.zeros(len(res))
termation = len(res) - 1
for i in range(endt + 50,len(res)):
    corre[i] = numpy.corrcoef((numpy.c_[res[endt-100:i+1],res1[endt-100:i+1]].T))[0][1]
    #===========================================================================
    # if(corre[i]<0.8):
    #     termation = i
    #     break
    #===========================================================================
plot(range(len(res)),corre)
show()

  
starts=numpy.zeros(len(res))
ends=numpy.zeros(len(res))
tes = (res + 500)/(res1 + 500)
pes = res - res1
#--------------------------------------------------------------------- tes = pes
plot(range(len(tes)),tes)
show()

# Creates lists containing values for Moving average-'movav' , Upper Bollinger band(2 std. dev.)-'bollhi', Lower Bollinger band(2 std. dev.)-'bolllo' 
movav=numpy.zeros(len(tes))
for i in range(len(tes)):
    if(i<dura):
        movav[i]=numpy.mean(tes[:i+1])
    else:
        movav[i]=numpy.mean(tes[i-dura:i+1])
bollhi=numpy.zeros(len(tes))
for i in range(len(tes)):
    if(i<dura):
        bollhi[i]=movav[i]+2*(numpy.std(tes[:i+1]))
    else:
        bollhi[i]=movav[i]+2*(numpy.std(tes[i-dura:i+1]))          
bolllo=numpy.zeros(len(tes))
for i in range(len(tes)):
    if(i<dura):
        bolllo[i]=movav[i]-2*(numpy.std(tes[:i+1]))
    else:
        bolllo[i]=movav[i]-2*(numpy.std(tes[i-dura:i+1]))        
  
  
# Locating start points and endpoints for trades according to the bollinger band strategy. 
# Enter the trade when tes moves beyond bollhi or bolllo and exit when tes touches moving average.
# All trades of type sell-buy, i.e., tes breaks beyond Upper Bollinger band are marked with 1. All trades of type buy-sell, i.e., tes breaks beyond Lower Bollinger band are marked with -1. By default all the rest of the points are marked 0.
temp_var=tes-bollhi
temp_var1=tes-bolllo
temp_var2=tes-movav
for i in range(len(tes)):
    if( (temp_var[i]>0) & (temp_var[i-1]<0) ):
        starts[i]=1
    if( (temp_var1[i-1]>0) & (temp_var1[i]<0) ):
        starts[i]=-1
    if( (temp_var2[i])*(temp_var2[i-1])<0 ):
        ends[i]=1
  
  

profacc=numpy.zeros(len(tes))
lossacc=numpy.zeros(len(tes))
P=[]
L=[]
A=[]
B=[]


it=endt # looking for trades starts just after training for fixed PCA.
investd = 0
numprof = 0 # number of profitable trades.
numloss = 0 # number of lossy trades.
while( it < termation ):
    j=0
    if(starts[it]==1):  # initiate trade when spread ratio exceeds the upper bollinger band.
        while(ends[it+j]==0):   # exits trade at the closest mean reverted point. records time of exit as 'it+j'.
            j=j+1
            if((it+j)==len(tes)-1):
                break

        # normalising the total trade at this point for an abstract investment of INR 1.00
        # total investment = total amount spending in buying the stocks(at start of trade = it) which are indicated for buying + total amount spent in buying back the stocks(at end of trade = it+j) which are indicated for selling. 
        norm = 0
        for i in range(len(clus[clusunsun])):
            if( (stknum[it][i]-store[i]) <0):
                norm = norm - ( (stknum[it][i]-store[i])*shet[i][it])
            else:
                norm = norm + ( (stknum[it][i]-store[i])*shet[i][it+j])
    
        earlier = pes[it]/norm
        later = numpy.dot( (stknum[it]-store)/norm , shet.T[it+j].T )
            
        if(earlier>later):  # case, when profit on the whole trade.
            profacc[it] = profacc[it] + numpy.abs(earlier - later)
            numprof = numprof + 1
            
        elif(earlier<later):    # case, when loss on the whole trade.
            lossacc[it] = lossacc[it] - numpy.abs(earlier - later)
            numloss = numloss + 1
            
    elif(starts[it]==-1):   # initiate trade when spread ratio goes below the lower bollinger band.
        while(ends[it+j]==0):   # exits trade at the closest mean reverted point. records time of exit as 'it+j'.
            j=j+1
            if((it+j)==len(tes)-1):
                break

        # normalising the total trade at this point for an abstract investment of INR 1.00
        # total investment = total amount spending in buying the stocks(at start of trade = it) which are indicated for buying + total amount spent in buying back the stocks(at end of trade = it+j) which are indicated for selling. 
        norm = 0
        for i in range(len(clus[clusunsun])):
            if( (stknum[it][i]-store[i]) <0):
                norm = norm - ( (stknum[it][i]-store[i])*shet[i][it])
            else:
                norm = norm + ( (stknum[it][i]-store[i])*shet[i][it+j])
    
        earlier = pes[it]/norm
        later = numpy.dot( (stknum[it]-store)/norm , shet.T[it+j].T )
        
        if(earlier<later):  # case, when profit on the whole trade.
            profacc[it] = profacc[it] + numpy.abs(earlier - later)
            numprof = numprof + 1
            
        elif(earlier>later):    # case, when loss on the whole trade.
            lossacc[it] = lossacc[it] - numpy.abs(earlier - later)
            numloss = numloss + 1
            
    else:
        j=0
    it=it+j+1       

 
print '\nprofit = ' + str(numpy.sum(profacc))
print 'loss = ' + str(-numpy.sum(lossacc))
print numprof
print numloss

plot(range(len(profacc)),profacc,'b')
show()
plot(range(len(lossacc)),lossacc,'r')
show()

plot(range(len(tes)),tes,'b')
plot(range(len(tes)),movav,'g')
plot(range(len(tes)),bollhi,'r')
plot(range(len(tes)),bolllo,'y')
# plot(range(len(res)),starts,'o')
# plot(range(len(res)),ends,'o')
plot(range(len(tes)),numpy.sign(profacc),'o')
plot(range(len(tes)),numpy.sign(lossacc),'o')
 
matplotlib.pylab.ylim(-40,40)
# matplotlib.pylab.xlim()
show()



#===============================================================================
# it=trainval-2
# while( it<1001 ):
#     j=0
#     if(starts[it]==1):
#         while(ends[it+j]==0):
#             j=j+1
#             if((it+j)==len(tes)-1):
#                 break
#         if(tes[it]>tes[it+j]):
#             profacc[it] = profacc[it] + numpy.abs(1-(tes[it+j]/tes[it])) # res[it]-res[it+j]
#         elif(tes[it]<tes[it+j]):
#             lossacc[it] = lossacc[it] - numpy.abs(1-(tes[it+j]/tes[it])) # res[it]-res[it+j]
#     elif(starts[it]==-1):
#         j=1
#         while(ends[it+j]==0):
#             j=j+1
#             if((it+j)==len(tes)-1):
#                 break
#         if(tes[it]<tes[it+j]):
#             profacc[it] = profacc[it] + numpy.abs(-1+(tes[it+j]/tes[it])) # -res[it]+res[it+j]
#         elif(tes[it]>tes[it+j]):
#             lossacc[it] = lossacc[it] - numpy.abs(-1+(tes[it+j]/tes[it])) # -res[it]+res[it+j]
#         
#     else:
#         j=0
#     it=it+j+1       
#===============================================================================
 
#===============================================================================
# it=trainval-2
# while( it<1001 ):
#     later = 0
#     j=0
#     if(starts[it]==1):
#         while(ends[it+j]==0):
#             j=j+1
#             if((it+j)==len(tes)-1):
#                 break
#         storeth = stknum[it] - store
#         for rain in range(len(storeth)):
#             later = later + storeth[rain]*shet[rain][it+j]
# 
#         if(pes[it]>later):
#             profacc[it] = profacc[it] + numpy.abs(1 - later/pes[it])
#         elif(pes[it]<later):
#             lossacc[it] = lossacc[it] - numpy.abs(1 - later/pes[it])
#     elif(starts[it]==-1):
#         j=1
#         while(ends[it+j]==0):
#             j=j+1
#             if((it+j)==len(tes)-1):
#                 break
#         storeth = stknum[it] - store
#         for rain in range(len(storeth)):
#             later = later + storeth[rain]*shet[rain][it+j]
# 
#         if(pes[it]<later):
#             profacc[it] = profacc[it] + numpy.abs(1 - later/pes[it])
#         elif(pes[it]>later):
#             lossacc[it] = lossacc[it] - numpy.abs(1 - later/pes[it])
#        
#     else:
#         j=0
#     it=it+j+1       
#===============================================================================
 
#===============================================================================
# it=trainval-2
# while( it< trainval + 512 ):
#     num1 = 0
#     num2 = 0
#     den1 = 0
#     den2 = 0
#     j=0
#     if(starts[it]==1):
#         while(ends[it+j]==0):
#             j=j+1
#             if((it+j)==len(tes)-1):
#                 break
#         
#         for rain in range(len(store)):
#             num1 = num1 + res1[it]*stknum[it][rain]*shet[rain][it+j]
#             den1 = den1 + res1[it]*stknum[it][rain]*shet[rain][it]
#             num2 = num2 + res[it]*store[rain]*shet[rain][it+j]            
#             den2 = den2 + res[it]*store[rain]*shet[rain][it]
#              
#         print '\n'
#         if((num2*den1)>(num1*den2)):
#             profacc[it] = profacc[it] + numpy.abs((num2/den2)-(num1/den1))
#         elif((num2*den1)<(num1*den2)):
#             lossacc[it] = lossacc[it] - numpy.abs((num2/den2)-(num1/den1))
#     elif(starts[it]==-1):
#         j=1
#         while(ends[it+j]==0):
#             j=j+1
#             if((it+j)==len(tes)-1):
#                 break
#         for rain in range(len(store)):
#             num1 = num1 + res1[it]*stknum[it][rain]*shet[rain][it+j]
#             den1 = den1 + res1[it]*stknum[it][rain]*shet[rain][it]
#             num2 = num2 + res[it]*store[rain]*shet[rain][it+j]            
#             den2 = den2 + res[it]*store[rain]*shet[rain][it]
#          
#         print '\n'
#         if((num2*den1)<(num1*den2)):
#             profacc[it] = profacc[it] + numpy.abs((num2/den2)-(num1/den1))
#         elif((num2*den1)>(num1*den2)):
#             lossacc[it] = lossacc[it] - numpy.abs((num2/den2)-(num1/den1))
#         
#     else:
#         j=0
#     it=it+j+1       
#===============================================================================
 
#----------------------------------------------------------------- it=trainval-2
#------------------------------------------------------------------- investd = 0
#-------------------------------------------------- while( it< trainval + 512 ):
    #----------------------------------------------------------------------- j=0
    #-------------------------------------------------------- if(starts[it]==1):
#------------------------------------------------------------------------------ 
        # #------------------------------------------------- investd = investd + 1
#------------------------------------------------------------------------------ 
        #------------------------------------------------- while(ends[it+j]==0):
            #------------------------------------------------------------- j=j+1
            #------------------------------------------- if((it+j)==len(tes)-1):
                #--------------------------------------------------------- break
#------------------------------------------------------------------------------ 
        #----------------------------------------------------------- earlier = 1
        #------------- later = dot( stknum[it]/res1[it],shet.T[it+j].T )/tes[it]
#------------------------------------------------------------------------------ 
        #--- investd = investd + 1#numpy.sum( numpy.abs( stknum[it]/res1[it] ) )
#------------------------------------------------------------------------------ 
        #---------------------------------------------------- if(earlier>later):
            #------------ profacc[it] = profacc[it] + numpy.abs(earlier - later)
#------------------------------------------------------------------------------ 
        #-------------------------------------------------- elif(earlier<later):
            #------------ lossacc[it] = lossacc[it] - numpy.abs(earlier - later)
#------------------------------------------------------------------------------ 
    #----------------------------------------------------- elif(starts[it]==-1):
#------------------------------------------------------------------------------ 
        # #------------------------------------------------- investd = investd + 1
#------------------------------------------------------------------------------ 
        #------------------------------------------------------------------- j=1
        #------------------------------------------------- while(ends[it+j]==0):
            #------------------------------------------------------------- j=j+1
            #------------------------------------------- if((it+j)==len(tes)-1):
                #--------------------------------------------------------- break
        #----------------------------------------------------------- earlier = 1
        #-------------- later = dot( stknum[it]/res[it],shet.T[it+j].T )/tes[it]
#------------------------------------------------------------------------------ 
        #--- investd = investd + 1#numpy.sum( numpy.abs( stknum[it]/res1[it] ) )
#------------------------------------------------------------------------------ 
        #---------------------------------------------------- if(earlier<later):
            #------------ profacc[it] = profacc[it] + numpy.abs(earlier - later)
        #-------------------------------------------------- elif(earlier>later):
            #------------ lossacc[it] = lossacc[it] - numpy.abs(earlier - later)
#------------------------------------------------------------------------------ 
    #--------------------------------------------------------------------- else:
        #------------------------------------------------------------------- j=0
    #----------------------------------------------------------------- it=it+j+1


