'''
Created on May 28, 2014

@author: admin
'''
import csv
import sklearn
import string
import numpy
from scipy import stats
import matplotlib.pylab
from sklearn.decomposition import PCA



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

for j in range(118):                                                                                        #for j in range(118):
    Matt[j]=  numpy.array( (  newk[j][1:]-numpy.mean(newk[j][1:])  )/numpy.std(newk[j][1:]) )                            #    Matt[j]=newk[j][1:]
    

     
pca=PCA(n_components=118)
pca.fit(Matt.T)

Zo = pca.components_


################################################################3

# MRFarr=numpy.array(newk[72][1:])
# 
# 
# newkarr=numpy.zeros([118,1023])
# for rain in range(118):
#     newkarr[rain]=numpy.array(newk[rain][1:])
# 
# for rain in range(118):
#     if(rain!=72):
#         newkarr[72]=newkarr[72]+(Zo[117][rain]*newkarr[rain])
# 
# expMRF=newkarr[72]


# matplotlib.pylab.plot(range(1023),MRFarr)                        #checked the goodness of approximation of MRF, by the rest of the stocks as PCs using PCA
# matplotlib.pylab.plot(range(1023),expMRF)
# matplotlib.pylab.show()



 

 

#Following has been turned to comments because data has been read and stored. It is done.

# file_open = open('PCA_olddatanew.csv', 'w')                                     #file_open = open('PCA_olddata.csv', 'w')
#   
# file_open.write('Principal components ,' + '(' + str(len(Zo)) + '),' + '\n\n')
#   
# for p in range(len(newk)):
#     file_open.write(newk[p][0] + ',')
#       
# file_open.write('\n')
#  
# for l in range(len(Zo)):
#     for m in range(len(Zo[0])):
#         file_open.write(str(Zo[l][m]) + ',')
#                           
#     file_open.write('\n')
#       
#       
#   
#       
# file_open.close()

#############################################################3

ClassA=[]
ClassB=[]
for q in range(len(newk)):
    if(Zo[0][q]<=0):               # high contribution stock printer
        ClassB.append(q)
    else:
        ClassA.append(q)
         
 
 
MattA=Matt[ClassA]
MattB=Matt[ClassB]        
  
MattA=MattA.T
  
       
pcaA=PCA(n_components=1)
pcaA.fit(MattA)
  
ZoA = pcaA.components_
  
MattB=MattB.T
  
       
pcaB=PCA(n_components=1)
pcaB.fit(MattB)
ZoB = pcaB.components_
 
 
# file_open.write('\n' + 'Class A,' + '(' + str(len(ZoA[0])) + '),' + '\n\n')
#            
# ctr=0
# l=0
# for ran in range(max(ClassA)+1):
#     if(ctr==ClassA[l]):
#         file_open.write(str(ZoA[0][l]) + ',')
#         l=l+1
#     else:
#         file_open.write(',')
#     ctr=ctr+1
#                                  
# file_open.write('\n')
#                
# file_open.close()
#   
#  
# file_open = open('PCA_olddata.csv', 'a')
#     
# file_open.write('\n' + 'Class B,' + '(' + str(len(ZoB[0])) + '),' + '\n\n')
#           
#           
# 
#  
# ctr=0
# m=0
# for ran in range(max(ClassB)+1):
#     if(ctr!=ClassB[m]):
#         file_open.write(',')
#     else:
#         file_open.write(str(ZoB[0][m]) + ',')
#         m=m+1
#     ctr=ctr+1
#                                 
# file_open.write('\n')
#                
# file_open.close()
