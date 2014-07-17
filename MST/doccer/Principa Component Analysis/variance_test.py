'''
Created on Jun 5, 2014

@author: admin
'''
import array
import csv
import numpy
from numpy import corrcoef
from numpy.linalg import det
import scipy
from scipy import stats
import matplotlib
from matplotlib.pylab import plot
from matplotlib.pylab import show
import sklearn
from sklearn.decomposition import PCA
from sklearn.cluster import spectral_clustering



with open('yawho.csv','rb') as f:
    rdr=csv.reader(f)
    k=[]
    for row in rdr:
        k.append(row)

print len(k)
print len(k[0]) 

k = k[2:]
print k
#   
# for i in range(,119):
#     for j in range(1,1024):
#         k[i][j]=float(k[i][j])
#          
# 
# newk=k[1: ]
# 
# 
# Matt=numpy.zeros([118,1023])
# 
# for j in range(118):
#     Matt[j]=newk[j][1:]-numpy.mean(newk[j][1:])
#     
# Matt=Matt[ : ,512: ]
# 
# pca=PCA(n_components=118)
# pca.fit(Matt.T)
# 
# Zo = pca.components_
# 
#     
# 
#   
# ################################################################3
# num=72
#    
# MRFarr=Matt[num]
#    
# expMRF=numpy.zeros(len(MRFarr))
# for rain in range(118):
#     if(rain!=num):
#         expMRF=expMRF-(Zo[117][rain]*Matt[rain])
# expMRF=expMRF/Zo[117][num]
#    
#    
#    
# # matplotlib.pylab.plot(range(1023),MRFarr,'g')                        #checked the goodness of approximation of MRF, by the rest of the stocks as PCs using PCA
# # matplotlib.pylab.plot(range(1023),expMRF,'b')
# # matplotlib.pylab.show()
#   
# yarr=MRFarr-expMRF
#     
# ymean=numpy.sqrt((numpy.mean(yarr*yarr))/ (len(Matt[0])-len(Matt)-1) )
#     
# def SE(rain):
#     xmean=numpy.mean(Matt[rain]*Matt[rain])
#     return ymean/(numpy.sqrt(xmean))
#  
#  
#  
# binchk=numpy.zeros(118)
#     
# tt_list=[]
# 
# 
# def stkfltr(sgval):
#     rainchk=[]
#     leftout=[]
#     for rainer in range(118):
#         tt=Zo[117][rainer]/SE(rainer)
#         tt=(-tt)/Zo[117][72]
#         if(len(tt_list)<len(Zo[0])):                                        #run only once, hence 'if-block'
#             tt_list.append(numpy.abs(tt))
#         pval = (stats.t.sf(numpy.abs(tt), (len(Matt[0])-len(Matt)-1)) )*2
#         if(pval>=sgval):
#             rainchk.append(rainer)
# #             binchk[rainer]=binchk[rainer]+1
# #             if(binchk[rainer]==1):
# #                 print newk[rainer][0]
#         else:
#             leftout.append(rainer)
#     return leftout
#     
# 
# sgval=1
# Listed=stkfltr(sgval)
# print len(Listed)
# Names=[] 
# for rin in range(len(stkfltr(sgval))):
#     Names.append(newk[Listed[rin]][0])
# #     print Names[rin]      
#      
#   
# arrformx=numpy.zeros([len(Listed),len(Matt[0])])
# for krain in range(len(Listed)):
#     arrformx[krain]=Matt[Listed[krain]]
#      
# cormtx=corrcoef(arrformx)   
# abscormtx=numpy.abs(cormtx)
# 
# # file_open = open('corrmatrixall.csv', 'a')    
# #    
# # for p in range(len(cormtx)):
# #     file_open.write(newk[Listed[p]][0] + ',')
# #  
# # file_open.write('\n')
# #      
# # for l in range(len(cormtx)):
# #     for m in range(len(cormtx[0])):
# #         file_open.write(str(cormtx[l][m]) + ',')
# #     file_open.write('\n')
# #     
# # file_open.write('\n\n')
# #           
# # file_open.close()
# 
# 
# 
# iterval=20
# plotter = numpy.zeros(iterval)
# plotter1 = numpy.zeros(iterval)
# 
# totalcorr=corrcoef(Matt)
# 
# ####
# for no_clusters in numpy.arange(2,len(plotter)+2):
#     
#     binall =  spectral_clustering(abscormtx,no_clusters)
#     
#     
#     septa=[]
#     numlist=[]
#     for i in range(no_clusters):
#         septa.append([])
#         numlist.append([])
#     
#     for i in range(len(binall)):
#         septa[binall[i]].append(Names[i])
#         numlist[binall[i]].append(Listed[i])
#     
#     if(no_clusters==4):
#         for i in range(4):
#             print len(numlist[i])
#         for i in range(4):
#             print septa[i]
#             
# 
#     resepta=[]
#     for i in range(no_clusters):
#         resepta.extend(numlist[i])
#     
#             
#     cluster_var=numpy.zeros(no_clusters)
#        
#     for i in range(no_clusters):
#         temparr=numpy.zeros([len(numlist[i]),len(Matt[0])])
#         for krain in range(len(numlist[i])):
#             temparr[krain]=Matt[numlist[i][krain]]
#         
#         tempcorr=corrcoef(temparr)    
#         tempcorr=numpy.abs(tempcorr)
#         
#         cluster_var[i]=numpy.var(tempcorr)
#     
#     mean_cluster_var=numpy.mean(cluster_var)
#     sum_cluster_var=numpy.sum(cluster_var)
#     
#     paired_var=numpy.zeros([no_clusters,no_clusters])
# 
#     for i in range(no_clusters):
#         for j in range(no_clusters):
#             if(i!=j):
#                 tempjoin=[]
#                 tempjoin.extend(numlist[i])
#                 tempjoin.extend(numlist[j])
#                 
#                 temparr=numpy.zeros([len(tempjoin),len(Matt[0])])
#                 for krain in range(len(tempjoin)):
#                     temparr[krain]=Matt[tempjoin[krain]]
# 
#                 tempcorr=corrcoef(temparr)    
#                 tempcorr=numpy.abs(tempcorr)
#             
#                 paired_var[i][j]=numpy.var( tempcorr[ :len(numlist[i]) , len(numlist[i]):len(tempjoin) ] )
#             
#     
#     mean_paired_var=(numpy.sum(paired_var))/((no_clusters)*(no_clusters-1))
#     sum_paired_var=numpy.sum(paired_var)
#     
#     plotter[no_clusters-2] = mean_cluster_var/mean_paired_var
#     plotter1[no_clusters-2] = sum_cluster_var/sum_paired_var
# 
#     
#     
# #     if(no_clusters==4):
# #         file_open = open('corrmatrixall.csv', 'w')
# #         
# #         for i in range(4):
# #             for j in range(len(numlist[i])):
# #                 file_open.write( str(numlist[i][j]) + ',' )
# #             file_open.write('\n')
# #                 
# #         file_open.write('\n')
# #         for i in range(4):
# #             helpcorr=numpy.zeros([len(numlist[i]),1023])
# #             for krain in range(len(numlist[i])):
# #                 helpcorr[krain]=Matt[numlist[i][krain]]
# #             helpcorr=corrcoef(helpcorr)    
# #             helpcorr=numpy.abs(helpcorr)
# #     
# #             
# #             for p in range(len(helpcorr)):
# #                 file_open.write(newk[ numlist[i][p] ][0] + ',')
# #             file_open.write('\n')
# # 
# #                  
# #             for l in range(len(helpcorr)):
# #                 for m in range(len(helpcorr[0])):
# #                     file_open.write(str(helpcorr[l][m]) + ',')
# #                 file_open.write('\n')
# #     
# #             file_open.write('\n\n')
# #           
# #         file_open.close()
#     
#     
# def inssort(this_list, that_elem):
#     this_list
#     if(this_list==[]):
#         this_list.append(that_elem)
#         return this_list
#     elif(that_elem>=this_list[-1]):
#         this_list.append(that_elem)
#         return this_list
#     else:
#         x=inssort(this_list[:-1], that_elem)
#         x.append(this_list[-1])
#         return x
#       
#   
# def sorter(act_list,switcheroo):
#     lust=[]
#     for i in range(len(act_list)):
#         lust=inssort(lust,act_list[i])
#         
#     if(switcheroo==0):
#         return lust
#       
#     ranker=range(len(act_list))
#     for i in range(len(act_list)):
#         for j in range(len(act_list)):
#             if(lust[i]==act_list[j]):
#                 ranker[i]=j
#                 act_list[j]=lust[0]-1
#                 break
#     else:        
#         return ranker
# 
# L=sorter(tt_list,1)
# 
# for i in L:
#     print newk[i][0]
# 
#     
# plot(range(len(plotter)),plotter)
# matplotlib.pylab.ylim(0,1)
# # plot(range(len(plotter1)),plotter1)
# show()
#     
#===============================================================================