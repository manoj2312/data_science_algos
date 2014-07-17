'''
Created on Jul 3, 2014

@author: manu
'''
import array
import csv
import numpy
from numpy import corrcoef
from numpy.linalg import det
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

compnum = 1
tt_main=[]

# Given the set of PCs obtained from the sklearn.decomposition.PCA as input, 'bestcomp' calculates the dimension along which there is maximum variation in the data set.
def bestcomp(peesee):   
    for i in range(len(peesee[0])):
        if(peesee[0][i]==max(peesee[0])):
            return i

# Given a series of values with missing values in between(0s), 'filler' smoothens the curve by calculating the average of the boundary values.        
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

# given an ordered list and an element to be inserted, the 'inssort' looks for the appropriate place for the element to be inserted in the list.
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

# Iterates 'inssort' over an unsorted list to form a sorted list. 'switcheroo' can take 0 or 1
# switcheroo = 0 : returns the sorted list.
# switcheroo = 1 : returns the index changes that were made to obtain  a sorted list. 
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


# Slope test- A statistical test which examines the significance of the linearity of the relation predicted by PCA. We need a dependent stock and a depend-on stock. We take the bestcomp stock as our dependent stock and the stock whose significance to be determined as depend-on stock.
# 'MRFarr' is the list of actual values of the bestcomp-stock. 'expMRF' is the list of expected values based on the PCA coefficients derived from the n-1 dimensional hyperplane of maximum variance.
# 'ymean' is calculated to further be incorporated in the calculation of Standard Error.
# SE = sqrt [ sigma(yi - Yi)^2 / (n - k - 1) ] / sqrt [ sigma(xi - x)^2 ]
def SE(rain,Mat,Zo):
    num=bestcomp(Zo)
    MRFarr=Mat[num]                    #MRFarr is the series of actual values of num-stock   
    expMRF=numpy.zeros(len(MRFarr))     #expMRF is the predicted series of values. Predicted using PCA
    for i in range(len(Mat)):
        if(i!=num):
            expMRF=expMRF-(Zo[compnum-1-1][i]*Mat[i])
    expMRF=expMRF/Zo[compnum-1-1][num]
    yarr=MRFarr-expMRF
    ymean=numpy.sqrt((numpy.mean(yarr*yarr))/(len(Mat[0])-len(Mat)-1))
    xmean=numpy.mean(Mat[rain]*Mat[rain])
    return ymean/(numpy.sqrt(xmean))

def stkfltr(sgval,Mat):
    tt_list=[]
    compnum=1                                                   #compnum represents the number corresponding to the PC of interest
    pca=PCA(n_components=len(Mat))
    pca.fit(Mat.T)
    Zo = pca.components_
    rainchk=[]
    leftout=[]
    for rainer in range(len(Zo)):
        if(rainer==bestcomp(Zo)):
            tt=1
        else:
            tt=Zo[compnum-1-1][rainer]/SE(rainer,Mat,Zo)
        tt=(-tt)/Zo[compnum-1-1][bestcomp(Zo)]
        if(len(tt_list)<len(Zo[0])):                                        #run only once, hence 'if-block'
            tt_list.append(numpy.abs(tt))
        pval = (stats.t.sf(numpy.abs(tt), len(Mat)-len(Zo[0])-1 ))*2
        if(pval>=sgval):
            rainchk.append(rainer)
#             binchk[rainer]=binchk[rainer]+1
#             if(binchk[rainer]==1):
#                 print newk[rainer][0]
        else:
            leftout.append(rainer)
    return tt_list
    #------------------------------------------------------------ return leftout

def stkr(sgval,Mat):                                      #Since the P-value (0.0242) is less than the significance level (0.05), there is significant linear relation
    compnum=1                                                   #compnum represents the number corresponding to the PC of interest
    pca=PCA(n_components=len(Matt))
    pca.fit(Matt.T)
    Zo = pca.components_
    rainchk=[]
    leftout=[]
    for rainer in range(len(Zo)):
        if(rainer==bestcomp(Zo)):
            tt=1
        else:
            tt=Zo[compnum-1-1][rainer]/SE(rainer,Mat)
        tt=(-tt)/Zo[compnum-1-1][bestcomp(Zo)]
        pval = (stats.t.sf(numpy.abs(tt), len(Mat)-len(Zo[0])-1 ))*2
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

def cutter(lis,which):
    return lis[:which] + lis[which+1:]

def contricalc(a1,a2,sheet,stoknum):
    X=numpy.zeros(len(stoknum))
    for i in range(len(stoknum)):
        X[i]=stoknum[i]*(sheet[i][a1]-sheet[i][a1+a2])
    X=X/(numpy.sum(X))
    X=100*X
    return X
     
def invhlth(a1,a2,sheet,stoknum,order):
    X=numpy.zeros(len(stoknum))
    if(order==0):
        for i in range(len(stoknum)):
            X[i]= numpy.sign(stoknum[i])*(1 - (sheet[i][a1+a2]/sheet[i][a1]))
    else:
        for i in range(len(stoknum)):
            X[i]= numpy.sign(stoknum[i])*(-1 + (sheet[i][a1+a2]/sheet[i][a1]))
         
    return X

#===============================================================================
# def movav(res,dur):
#     rarr=numpy.zeros(len(res))
#     for i in range(len(res)):
#         if(i<dur):
#             rarr[i]=numpy.mean(res[:i+1])
#         else:
#             rarr[i]=numpy.mean(res[i-dur:i+1])
#     return rarr 
#  
# def bollhi(res,dur):
#     rarr=numpy.zeros(len(res))
#     for i in range(len(res)):
#         if(i<dur):
#             rarr[i]=movav(res,dur)[i]+2*(numpy.std(res[:i+1]))
#         else:
#             rarr[i]=movav(res,dur)[i]+2*(numpy.std(res[i-dur:i+1]))        
#     return rarr
#  
# def bolllo(res,dur):
#     rarr=numpy.zeros(len(res))
#     for i in range(len(res)):
#         if(i<dur):
#             rarr[i]=movav(res,dur)[i]-2*(numpy.std(res[:i+1]))
#         else:
#             rarr[i]=movav(res,dur)[i]-2*(numpy.std(res[i-dur:i+1]))        
#     return rarr
#===============================================================================
