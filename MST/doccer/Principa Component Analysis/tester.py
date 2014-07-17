'''
Created on May 27, 2014

@author: admin
'''

import csv
import sklearn
import string
import numpy
from numpy import dot
from scipy import stats
import matplotlib
from matplotlib.pylab import plot
from matplotlib.pylab import show
from sklearn.decomposition import PCA
from sklearn.cluster import spectral_clustering
from numpy import corrcoef
from mpl_toolkits.mplot3d import axes3d


# 
# 
# pca=decomposition.PCA()
# pca.fit(X).transform(X)
#   
# cf=pca.explained_variance_
#   
# k=numpy.arange(-0.5,0.5,20)
# k1= -(cf[0]/cf[1])*k
#   
# matplotlib.pylab.plot(X[0].T,X[1].T,'o')
#   
# matplotlib.pylab.plot(k,k1,'.')
#   
# matplotlib.pylab.show()



# m=3
#  
# x=numpy.arange(0,100,1)
#  
# err=numpy.zeros(100)
# for k in range(100):
#     err[k]=numpy.random.rand()


# Matt=numpy.zeros([3,3])
# 
# Matt[1]=Matt[1]-3
# print Matt


# x=numpy.arange(-5,6,0.1)
# y=numpy.abs(x)
# print y

# septa=[]
# for i in range(4):
#     septa.append([])
#     
# print septa


# a=numpy.zeros([3,4])
# a[0]=1
# print a[0][1]
# print a[1][0]
# print a


# a=numpy.zeros([3,4])
# a[0]=1
# a[1]=2
# a[2]=3
# 
# print a
# print numpy.mean(a)
# print numpy.sum(a)


# print str( (118.0**2.0)*(1.0/2.0) )
# print str( (118.0**2.0)*(2.0/3.0) )
# print str( (118.0**2.0)*(3.0/4.0) )
# print str( (118.0**2.0)*(4.0/5.0) )


# A=[1,2,2,2,2,2,3]
# print numpy.var(A)
# print numpy.sqrt(numpy.var(A))
# print numpy.std(A)
# 
# 
# A=[1,2,3]
# B=[0,5]
# print numpy.var(A)
# print numpy.var(B)
# print A + B

# a=numpy.zeros([3,4])
# a[0]=1
# a[1]=2
# a[2]=3
# 
# print a
# print a[0:]


# a=numpy.zeros([3,4])
# a[0]=1
# a[1]=2
# a[2]=3
# numlist=[0,2]
# print a[numlist]


# print int(22.0/7.0)


# gstr= 'hellooool'
# print gstr[4]


# bstr='35'
# print bstr
# print int(bstr)
# print  int(bstr) + 3
# print bstr+3

# numlist=''
# x= (numlist=='')
# print x



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
# # L=[1,2,4,5,6]
# # print L
# # print inssort(L,3)
# # print L
# 
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
# # L=[3,4,1,8,3,6,5,8,9,7,6,4,2]
# # print sorter(L,0)
# # print L
# # print sorter(L,1)



# tt=0.1
# print (stats.t.sf(numpy.abs(tt), 1))*2
# tt=-0.1
# print (stats.t.sf(numpy.abs(tt), 1))*2



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
    Matt[j]=(newk[j][1:])#-numpy.mean(newk[j][1:]))/numpy.std(newk[j][1:])
     
# # plot(range(1023),Matt[72])#mrf
# # plot(range(1023),Matt[33])#dabur
# # plot(range(1023),Matt[44])#havells
# # plot(range(1023),Matt[19])
# # show()
# 
# # X=numpy.zeros([3,1023])
# # X[0]=Matt[72]
# # X[1]=Matt[33]
# # X[2]=Matt[44]
# # # print corrcoef(X)
# # 
# # pca=PCA(n_components=3)
# # pca.fit(X.T)
# # coff=pca.components_[2]
# # 
# # matplotlib.figure.Figure()
# # m=numpy.arange(min(X[0]),max(X[0]))
# # h=numpy.arange(min(X[2]),max(X[2]))
# # M,H=numpy.meshgrid(m,h)
# # D=numpy.zeros([numpy.shape(M)[0],numpy.shape(M)[1]])
# # print D.shape
# # for i in range(len(D)):
# #     for j in range(len(D[0])):
# #         D[i][j]=(-coff[0]/coff[1])*m[j] + (-coff[2]/coff[1])*h[i]
# # ax=axes3d.Axes3D
# # surf = ax.plot_surface(H, M, D, rstride=1, cstride=1)


# stash=[75, 117, 7, 29, 78, 107, 114, 68, 74, 103, 41, 28, 54, 84, 79]
# L=[]
# for i in range(len(stash)):
#     L.append(stash[-i-1])
# print L



# X=newk[:3]
# print X
# print X.T



# A='what is it?'
# B='what is it?'
# if(A==B):
#     print 'yeaaaa!!!'


#===============================================================================
# leftout =[]
# # find = [43, 8, 0, 87, 32, 24, 19, 48, 69, 30, 33, 80, 92, 86, 72, 7, 5, 75, 83, 18, 11, 53, 35, 14, 23, 39, 58, 46, 90, 27, 21, 88, 36, 81, 85, 63, 37, 47, 2, 42, 57, 64, 49, 43, 8, 87, 0, 80, 24, 32, 48, 19, 28, 69, 92, 12, 33, 72, 30, 86, 9, 57, 39, 63, 13, 70, 42, 31, 46, 49, 64, 73, 85, 2, 47, 52, 29, 59, 65, 84, 38, 82, 44, 10, 22, 41, 16, 3, 34, 15, 61, 54, 78, 67, 71, 26, 90]
# # find = [43, 8, 0, 87, 32, 24, 19, 48, 69, 30, 33, 80, 92, 86, 72, 7, 5, 75, 83, 18, 11, 53, 35, 14, 23, 39, 58, 46, 90, 27, 21, 88, 36, 81, 85, 63, 37, 47, 2, 42, 57, 64, 49, 43, 8, 87, 0, 80, 24, 32, 48, 19, 28, 69, 92, 12, 33, 72, 30, 86, 9, 57, 39, 63, 13, 70, 42, 31, 46, 49, 64, 73, 85, 2, 47, 52, 29, 59, 65, 84, 38, 82, 44, 10, 22, 41, 16, 3, 34, 15, 61, 54, 78, 67, 71, 26, 90, 25, 74, 48, 24, 91, 10, 68, 19, 92, 8, 27, 17, 37, 82, 33, 81, 9, 57, 39, 63, 13, 70, 42, 31, 46, 49, 64, 73, 85, 2, 47, 80, 43, 0, 69, 87, 30, 32, 72, 86, 26, 71, 61, 54, 15, 67, 34]
# find = [9, 39, 57, 70, 63, 13, 31, 42, 46, 49, 64, 58, 73, 85, 2, 47, 44, 52, 84, 65, 51, 59, 41, 16, 3, 22, 78, 71, 61, 38, 67, 15, 26, 54, 34, 43, 8, 0, 87, 32, 24, 19, 69, 48, 30, 33, 80, 86, 72, 78, 42, 63, 47, 73, 31, 49, 70, 2, 13, 9, 7, 5, 75, 83, 18, 11, 53, 35, 14, 23, 6, 29, 4, 52, 20, 12, 28, 79, 16, 77, 56, 41, 3, 38, 15, 71, 90, 54, 26, 34, 67, 85, 57, 46, 64, 37, 39, 81, 43, 8, 87, 0, 80, 24, 32, 19, 48, 28, 12, 69, 92, 33, 30, 20, 86, 72, 34, 78, 16, 15, 67, 71, 26, 54, 56, 38, 40, 76, 89, 27, 36, 55, 60, 45, 77, 21, 88]
# for i in range(len(find)):
#     for j in find:
#         if(i==j):
#             i=-1
#             break
#     if(i!=-1):
#         leftout.append(i)
#         
# print leftout        
#===============================================================================


