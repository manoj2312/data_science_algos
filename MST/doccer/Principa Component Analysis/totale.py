'''
Created on Jun 11, 2014

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
import matplotlib 
from matplotlib.pylab import plot
from matplotlib.pylab import show
from sklearn.decomposition import PCA
from sklearn.cluster import spectral_clustering
from numpy import corrcoef


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

#read data from file and store in matrices 
with open('Mean_Reversion_strategy_data_PRICES.csv','rb') as f:
    rdr=csv.reader(f)
    k=[]
    for row in rdr:
        k.append(row)
    
for i in range(1,len(k)):
    for j in range(1,len(k[0])):
        k[i][j]=float(k[i][j])
newk=k[1: ]
 
Matt=numpy.zeros([len(k)-1,len(k[0])-1])                    #Matt is the array filled with float values with values of one stock in a column
for j in range(len(Matt)):
    Matt[j]=newk[j][1:]-numpy.mean(newk[j][1:])
     

#finding PCA for all stocks
compnum=1                                                   #compnum represents the number corresponding to the PC of interest
pca=PCA(n_components=len(Matt))
pca.fit(Matt.T)
Zo = pca.components_


#finding stock with largest component in the first PC and then doing slope test on each other stock with the num-stock as the dependent series 
def bestcomp(peesee):
    for i in range(len(peesee[0])):
        if(peesee[0][i]==max(peesee[0])):
            return i


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
 
# binchk=numpy.zeros(118)
tt_main=[]
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
    tt_main.append(tt_list)
    return leftout

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



#deciding number of clusters
iterval=20
plotter = numpy.zeros(iterval)
plotter1 = numpy.zeros(iterval)

cormtx=corrcoef(Matt)   
abscormtx=numpy.abs(cormtx)
for no_clusters in numpy.arange(2,len(plotter)+2):
    
    binall =  spectral_clustering(abscormtx,no_clusters)
    
    septa=[]
    numblist=[]
    for i in range(no_clusters):
        septa.append([])
        numblist.append([])
    
    for i in range(len(binall)):
        septa[binall[i]].append(newk[i][0])
        numblist[binall[i]].append(i)
    
#     if(no_clusters==4):
#         for i in range(4):
#             print len(numblist[i])
#         for i in range(4):
#             print septa[i]
            

    resepta=[]
    for i in range(no_clusters):
        resepta.extend(numblist[i])
    
    cluster_var=numpy.zeros(no_clusters)
    for i in range(no_clusters):
        temparr=numpy.zeros([len(numblist[i]),1023])
        for krain in range(len(numblist[i])):
            temparr[krain]=Matt[numblist[i][krain]]
        tempcorr=corrcoef(temparr)    
        tempcorr=numpy.abs(tempcorr)       
        cluster_var[i]=numpy.var(tempcorr)
        
    mean_cluster_var=numpy.mean(cluster_var)
    sum_cluster_var=numpy.sum(cluster_var)
    
    paired_var=numpy.zeros([no_clusters,no_clusters])
    for i in range(no_clusters):
        for j in range(no_clusters):
            if(i!=j):
                tempjoin=[]
                tempjoin.extend(numblist[i])
                tempjoin.extend(numblist[j])
                
                temparr=numpy.zeros([len(tempjoin),1023])
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

binall =  spectral_clustering(abscormtx,no_clusters)
numlist=[]
for i in range(no_clusters):
    numlist.append([])    
for i in range(len(binall)):
    numlist[binall[i]].append(i)

for i in range(no_clusters):
    print len(numlist[i])

#         file_open = open('corrmatrixall.csv', 'w')
#         
#         for i in range(no_clusters):
#             for j in range(len(numlist[i])):
#                 file_open.write( str(numlist[i][j]) + ',' )
#             file_open.write('\n')
#                 
#         file_open.write('\n')
#         for i in range(no_clusters):
#             helpcorr=numpy.zeros([len(numlist[i]),len(Matt[0])])
#             for krain in range(len(numlist[i])):
#                 helpcorr[krain]=Matt[numlist[i][krain]]
#             helpcorr=corrcoef(helpcorr)    
#             helpcorr=numpy.abs(helpcorr)
#     
#             
#             for p in range(len(helpcorr)):
#                 file_open.write(newk[ numlist[i][p] ][0] + ',')
#             file_open.write('\n')
# 
#                  
#             for l in range(len(helpcorr)):
#                 for m in range(len(helpcorr[0])):
#                     file_open.write(str(helpcorr[l][m]) + ',')
#                 file_open.write('\n')
#     
#             file_open.write('\n\n')
#           
#         file_open.close()

   
# with open('corrmatrixall.csv','rb') as f:
#     rdr=csv.reader(f)
#     numlist=[]
#     i=0
#     for row in rdr:
#         if(i<4):
#             numlist.append(row)
#         else:
#             break
#         i=i+1
#          
# for i in range(len(numlist)):
#     for j in range(len(numlist[i])):
#         if(numlist[i][j]==''):
#             numlist[i]=numlist[i][:j]
#             break
#         else:
#             numlist[i][j] = int(numlist[i][j])
  
numsort=numpy.zeros(len(numlist))
for i in range(len(numlist)):
    numsort[i]=len(numlist[i])
ranked=sorter(numsort,1)
copy=numlist
numlist=[]
for i in range(no_clusters):
    numlist.append([])    
for i in range(no_clusters):
    numlist[i]=copy[ranked[i]]

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
    numer[j]=bestcomp(Zoer[j])

MRFarr=numpy.zeros([no_clusters,len(Matt[0])])
 
for i in range(no_clusters):
    #print newk[numlist[i][numer[i]]][0]
    MRFarr[i] = Matter[i][numer[i]]
    
expMRF=numpy.zeros([no_clusters,len(Matt[0])])
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

for i in range(no_clusters):
    stkfltr(numpy.random.rand(),Matter[i])



tember=[]
for i in range(no_clusters):
    temb=[]
    L=sorter(tt_main[i],1)
    for j in L:
#         print newk[numlist[i][j]][0]
        temb.append(numlist[i][j])
    tember.append(temb)
    
    

# 
# slash=[72, 33, 56, 44, 19, 9, 13, 104, 1, 69, 43, 57, 82, 5, 37, 42, 16, 87, 70, 11, 102, 116, 62, 30, 108, 0, 49, 35, 73, 45, 34, 40, 71, 51, 110, 22, 46, 23, 26, 101, 97, 2]
# # slash=[63, 12, 47, 4, 10, 27, 52, 20, 60, 61, 91, 99, 15, 80, 94, 115, 53, 86, 8, 106, 48, 17, 31, 6, 98, 95, 3, 67, 18, 100, 93, 85, 38, 14, 24, 64, 111, 36, 109]
# # slash=[89, 112, 105, 66, 55, 39, 59, 77, 76, 90, 88, 50, 113, 21, 25, 32, 92, 65, 58, 81, 83, 96]
# # slash=[79, 84, 54, 28, 41, 103, 74, 68, 114, 107, 78, 29, 7, 117, 75]


#tember is set of slash-es. which are t ordered clusters
#clusunsun-th cluster is under scrutiny
#after for-loop, slashet is the set of stocks selected from the cusunsun-th cluster
#after for-loop, res is the residual resulted from the PC sum of the selected stocks

storeth=[]
clusunsun=3


#===============================================================================
# for i in range(len(Zoer[clusunsun])-2):
#     res=numpy.zeros(len(Matt[0]))
#     slashet=tember[clusunsun][:3+i]
#     pca=PCA(n_components=len(slashet))
#     shet=Matt[slashet]
#     pca.fit(shet.T)
#     storeth.append(pca.components_[compnum-1-1])
#     for j in range(len(shet[0])):
#         for ij in range(len(storeth[-1])):
#             res[j]=res[j]+storeth[-1][ij]*shet[ij][j]
# #     if(i==0):
# #         break
# #     print numpy.mean(res)
#  
#     if(adfuller(res, maxlag=None, regression='c', autolag='AIC', store=False, regresults=False)[0] <=-4.5):
#         break
#  
# stknum=storeth[-1]
# print stknum
#===============================================================================



for i in range(len(Zoer[clusunsun])-2):
    stknum=[]
    res=numpy.zeros(len(Matt[0]))
    res1=numpy.zeros(len(Matt[0]))
    slashet=tember[clusunsun][:3+i]
    shet=Matt[slashet]

    pca=PCA(n_components=len(slashet))
    pca.fit(shet[:,:512].T)
    store = pca.components_[compnum-1-1]
    for j in range(len(shet[0])):
        for ij in range(len(slashet)):
            res1[j]=res1[j]+store[ij]*shet[ij][j]

    for j in range(len(shet[0])):
        storeth=[]
        for ij in range(len(slashet)):
            pca=PCA(n_components=len(slashet))
            pca.fit(shet[:,:j+1].T)
            tmpor = pca.components_[-1]
            if(numpy.dot(tmpor,store)<0):
                storeth.append(-tmpor)
            else:
                storeth.append(tmpor)
                
#             rectify = store[0]-pca.components_[compnum-1-1][0]
#             clerity = store[0]+pca.components_[compnum-1-1][0]
#             if( numpy.dot(rectify,rectify.T) < numpy.dot(clerity,clerity.T) ):
#                 storeth.append( pca.components_[compnum-1-1] )
#             else:
#                 storeth.append( -pca.components_[compnum-1-1] )
            res[j]=res[j]+storeth[-1][ij]*shet[ij][j]
        stknum.append(storeth[-1])
    if( min(adfuller(res[300:], maxlag=None, regression='c', autolag='AIC', store=False, regresults=False)[0], adfuller(res1, maxlag=None, regression='c', autolag='AIC', store=False, regresults=False)[0]) <=-4.5) :
        break
print store



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



movav=numpy.zeros(len(res))
bollhi=numpy.zeros(len(res))
bolllo=numpy.zeros(len(res))


for i in range(len(res)):
    if(i<19):
        movav[i]=numpy.mean(res[:i+1])
        bollhi[i]=movav[i]+2*(numpy.std(res[:i+1]))
        bolllo[i]=movav[i]-2*(numpy.std(res[:i+1]))
    else:
        movav[i]=numpy.mean(res[i-19:i+1])
        bollhi[i]=movav[i]+2*(numpy.std(res[i-19:i+1]))
        bolllo[i]=movav[i]-2*(numpy.std(res[i-19:i+1]))        



starts=numpy.zeros(len(res))
ends=numpy.zeros(len(res))

temp_var=res-bollhi
temp_var1=res-bolllo
temp_var2=res-movav
for i in range(len(res)):
    if( (temp_var[i]>0) & (temp_var[i-1]<0) ):
        starts[i]=1
    if( (temp_var1[i-1]>0) & (temp_var1[i]<0) ):
        starts[i]=-1
    if( (temp_var2[i])*(temp_var2[i-1])<0 ):
        ends[i]=1




profacc=numpy.zeros(len(res))
lossacc=numpy.zeros(len(res))
P=[]
L=[]
A=[]
B=[]


#===============================================================================
# it=0
# while(it<len(res)):
#     j=0
#     if(starts[it]==1):
#         while(ends[it+j]==0):
#             j=j+1
#             if((it+j)==len(res)-1):
#                 break
#         if(res[it]>res[it+j]):
#             profacc[it] = profacc[it] + res[it]-res[it+j]
#             P.append(contricalc(it,j,shet,stknum))
#             A.append(invhlth(it,j,shet,stknum,0))
#         elif(res[it]<res[it+j]):
#             lossacc[it] = lossacc[it] + res[it]-res[it+j]
#             L.append(contricalc(it,j,shet,stknum))
#             B.append(invhlth(it,j,shet,stknum,0))
#     elif(starts[it]==-1):
#         j=1
#         while(ends[it+j]==0):
#             j=j+1
#             if((it+j)==len(res)-1):
#                 break
#         if(res[it]<res[it+j]):
#             profacc[it] = profacc[it] + res[it+j]-res[it]
#             P.append(contricalc(it,j,shet,stknum))
#             A.append(invhlth(it,j,shet,stknum,1))
#         elif(res[it]>res[it+j]):
#             lossacc[it] = lossacc[it] + res[it+j]-res[it]
#             L.append(contricalc(it,j,shet,stknum))
#             B.append(invhlth(it,j,shet,stknum,1))
#      
#     else:
#         j=0
#     it=it+j+1       
#===============================================================================
            
it=300
while(it<len(res)):
    j=0
    if(starts[it]==1):
        while(ends[it+j]==0):
            j=j+1
            if((it+j)==len(res)-1):
                break
        if(res[it]>res[it+j]):
            profacc[it] = profacc[it] + res[it]-res[it+j]
#             P.append(contricalc(it,j,shet,stknum[it]))
            A.append(invhlth(it,j,shet,stknum[it],0))
        elif(res[it]<res[it+j]):
            lossacc[it] = lossacc[it] + res[it]-res[it+j]
#             L.append(contricalc(it,j,shet,stknum[it]))
            B.append(invhlth(it,j,shet,stknum[it],0))
    elif(starts[it]==-1):
        j=1
        while(ends[it+j]==0):
            j=j+1
            if((it+j)==len(res)-1):
                break
        if(res[it]<res[it+j]):
            profacc[it] = profacc[it] + res[it+j]-res[it]
#             P.append(contricalc(it,j,shet,stknum[it]))
            A.append(invhlth(it,j,shet,stknum[it],1))
        elif(res[it]>res[it+j]):
            lossacc[it] = lossacc[it] + res[it+j]-res[it]
#             L.append(contricalc(it,j,shet,stknum[it]))
            B.append(invhlth(it,j,shet,stknum[it],1))
    
    else:
        j=0
    it=it+j+1       


print '\nprofit = ' + str(numpy.sum(profacc))
print 'loss = ' + str(-numpy.sum(lossacc)) + '\n'

A=numpy.array(A)
B=numpy.array(B)
A=A.T
B=B.T

for i in range(len(slashet)):
    print str(newk[slashet[i]][0]) + '\nprofits: ' + str(numpy.sum(A[i])) + '\t\t\t\tlosses: ' + str(numpy.mean(B[i])) 

# Pr=numpy.zeros([len(P),len(slashet)])
# Lo=numpy.zeros([len(L),len(slashet)])
# for i in range(len(P)):
#     Pr[i]=P[i]
# for i in range(len(L)):
#     Lo[i]=L[i]
# Pr=Pr.T
# Lo=Lo.T
# for i in range(len(slashet)):
#     print str(newk[slashet[i]][0]) + '\nave. % contr to profits: ' + str(numpy.mean(Pr[i])) + '\t\t\t\t\tave. % contr to losses: ' + str(numpy.mean(Lo[i])) 

    
plot(range(len(res)),res)
plot(range(len(res)),movav)
plot(range(len(res)),bollhi)
plot(range(len(res)),bolllo)
# plot(range(len(res)),starts,'o')
# plot(range(len(res)),ends,'o')
plot(range(len(res)),numpy.sign(profacc),'o')
plot(range(len(res)),numpy.sign(lossacc),'o')

matplotlib.pylab.ylim(-20,20)
matplotlib.pylab.xlim(0,1023)
show()


plot(range(len(res)),res,'r')
plot(range(len(res)),res1,'g')
matplotlib.pylab.ylim(-50,50)
show()

