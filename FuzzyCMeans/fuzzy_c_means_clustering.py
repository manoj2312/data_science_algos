"""
data_matrix: should be numpy.ndarray and the each row represents a data point and each column is a property of the prepared sand
cluster_centers_new : is a numpy.ndarray and each row represents a cluster center and each column is a property of the prepared sand
distance_matrix : is a numpy.ndarray and each row represents distance between a cluster center and all the data points,
                  each column represents distance of a data point from all cluster centers
membership_matrix: is a numpy.ndarray and each row represents membership of each data point to a particular cluster center,
                     each column represents membership of a data point to all cluster centers
"""

import random
import numpy
import copy
import math
from matplotlib import pyplot

def load_into_file(path,header=True):
        # input of this function - 'path' is a variable which tells us the location where the data file is located
        # ouput of this function - looks like a matrix (it will be a list of lists)
    File=open(path,'r')
    lines=File.readlines()
    final_list=[]
    for line in lines:
            final_list.append([float(i) for i in line.split('\t')])
    File.close()
    return final_list
def fuzzy_c_means(data_matrix,num_cluster_centers,q=2,tol=.0001,num_iter=10):
    """
    This function will do the fuzzy c means clustering for input data 
    
    @param data_matrix: contains the input data in an array format
    @param num_cluster_centers: number of cluster centers that needs to be computed
    @param q: fuzzifier value
    @param tol: tolerance between old and new cluster centers
    @precondition: data_matrix is an array 
    @return: return arrays of new cluster centers and membership matrix
    @todo: 
    
    """     
    input_data = copy.deepcopy(data_matrix)
    dim = input_data.shape[1]
    num_of_data_points = input_data.shape[0]
    
    ' storing cluster_centers,membership_matrix,objective_function in each iteration'
    cluster_centers_iteration = []
    membership_matrix_iteration = []
    fcm_obj_fn_value_iteration = []
    for iter in range(num_iter):
        cluster_centers_new = numpy.zeros((num_cluster_centers,dim))
        membership_matrix = numpy.zeros((num_cluster_centers,num_of_data_points))
        distance_matrix = numpy.zeros((num_cluster_centers,num_of_data_points))
        cluster_centers_new = initial_clusters(num_cluster_centers,input_data)
        while(True):
            distance_matrix = compute_distance_matrix(input_data,cluster_centers_new)
            membership_matrix = compute_membership_matrix(distance_matrix,q)
            cluster_centers_old = copy.deepcopy(cluster_centers_new)
            cluster_centers_new = update_cluster_center(input_data,cluster_centers_new,membership_matrix,q)
            flag = 0
            for i in range(num_cluster_centers):
                if(numpy.linalg.norm(cluster_centers_new[i] - cluster_centers_old[i]))>tol:
                    flag = 1
            if flag == 0:
                break
        obj_fn_value = fcm_objective_function_value(membership_matrix,distance_matrix,q)
        cluster_centers_iteration.append(cluster_centers_new)
        membership_matrix_iteration.append(membership_matrix)
        fcm_obj_fn_value_iteration.append(obj_fn_value)
    
    ' identifying the iteration which has minimum objective function value'
    min_obj_fn_index = fcm_obj_fn_value_iteration.index(min(fcm_obj_fn_value_iteration))
    cluster_centers_final = cluster_centers_iteration[min_obj_fn_index]
    membership_matrix_final = membership_matrix_iteration[min_obj_fn_index]
    return (cluster_centers_final, membership_matrix_final)

    
def initial_clusters(num_cluster_centers,input_data):
    """ 
    randomly generate cluster centers from upper and lower bounds of input data matrix
    
    @param num_cluster_centers : number of cluster centers
    @param input_data : contains input data in a matrix format
    @precondition: 
    @return : returns an array with initial clusters randomly generated from the scaling data 
    @todo :  
      
    """
    dim = input_data.shape[1]
    scaling_data = numpy.vstack((input_data.min(axis = 0),input_data.max(axis = 0)))
    cluster_centers_new = numpy.zeros((num_cluster_centers,dim))
    for i in range(num_cluster_centers):
        for j in range(dim):
              cluster_centers_new[i][j] = random.uniform(scaling_data[0][j],scaling_data[1][j])              
    return cluster_centers_new 


def compute_distance_matrix(input_data,cluster_centres_new):
    """
    computes distance between a cluster center and data point
    
    @param input_data: contains input data in a matrix format
    @param cluster_centres_new:array with newly generated cluster centers 
    @return: function returns the array with distance between a cluster center and a data point as its elements
    @todo: 
    
    """
    num_cluster_centers = cluster_centres_new.shape[0]
    num_of_data_points = input_data.shape[0]
    distance_matrix = numpy.zeros((num_cluster_centers,num_of_data_points))
    for i in range(num_cluster_centers):
            for j in range(num_of_data_points):
                distance_matrix[i][j] = numpy.linalg.norm([cluster_centres_new[i] - input_data[j]])                
    return distance_matrix


def compute_membership_matrix(distance_matrix,q):
    """ 
    compute membership for each data point with respect to a cluster center
    
    @param distance_matrix: array with distance between a cluster center and a data point as its elements
    @param q:fuzzifier value
    @return: membership of a each data point to a cluster center
    @todo: 
    
    """
    num_of_data_points =  distance_matrix.shape[1]
    num_cluster_centers = distance_matrix.shape[0]
    membership_matrix = numpy.zeros((num_cluster_centers,num_of_data_points))
    for i in range(num_cluster_centers):
            total = 0
            for j in range (num_of_data_points):
                total = sum((float(1) / distance_matrix[:,j])**(2/(q-1)))
                total = 1 / total
                membership_matrix[i][j] = (float(1) / ((distance_matrix[i][j]) ** (2 / (q-1)))) * total
    return membership_matrix

  
def update_cluster_center(input_data,cluster_centers_new,membership_matrix,q):
    """ 
    will update the cluster centers with new membership values
    
    @param input_data: array with input data points
    @param cluster_centers_new:array with newly computed cluster centers  
    @param membership_matrix: matrix containing membership of each data point to a cluster center
    @param q: fuzzifier value
    @return: updated cluster centers 
    @todo: 
       
    """
    dim = cluster_centers_new.shape[1]
    num_cluster_centers = cluster_centers_new.shape[0]
    num_of_data_points = membership_matrix.shape[1]
    for i in range(num_cluster_centers):
             denom = 0
             numer = numpy.zeros(dim)
             for j in range(num_of_data_points):
                 numer = numer + ((membership_matrix[i][j]) ** q) * input_data[j] 
                 denom = denom + (membership_matrix[i][j]) ** q
             cluster_centers_new[i] = numer / denom                         
    return cluster_centers_new  
        
             
def perform_reassigning(cluster_centers,membership_matrix,input_data,q=2,factor=1.5):
        """
        will check for minimum no of points in each cluster. for all those clusters having number of points less than threshold value, cluster center is removed
        and the points associated with those cluster centers are distributed among the remaining clusters. This distribution is done my calculating membership matrix
        with the remaining cluster centers.
        
        @param cluster_centers : array of cluster centers returned by fuzzy_c_means function
        @param membership_matrix : array of membership value of each data point  w.r.t to cluster centers
        @param input_data :array with input data points
        @param q : fuzzifier value   
        @param factor: factor to get the minimum no of points needed to retain a cluster center
        @return: new cluster centers and membership matrix after reassigning is done
        @todo: 
               
        """
        num_of_data_points = input_data.shape[0]
        dim = input_data.shape[1]
        min_pts_factor = int(dim*factor)
        while (True):
            num_cluster_centers,cluster_distribution = compute_clusters_and_distribution(membership_matrix)
            count = 0
            iter_list = reassigning_indices_order(cluster_distribution)
            for key in iter_list:
                count_num_points = sum(cluster_distribution[key])
                if count_num_points < int(min_pts_factor):
                    membership_matrix,cluster_centers = reassigning_cluster(cluster_centers,key,input_data,q)
                    break
                count+= 1
            if count == num_cluster_centers:
                break
        num_cluster_centers = cluster_centers.shape[0]
        distance_matrix = compute_distance_matrix(input_data,cluster_centers)
        membership_matrix_new = compute_membership_matrix(distance_matrix,q)        
        return ( cluster_centers , membership_matrix_new )   
       
            
def compute_clusters_and_distribution(mu_new):
    """
    will assign data points with maximum membership w.r.t a cluster center to that cluster center. It will do the same by 
           giving membership to that particular cluster center as 1 and to remaining cluster centers as 0
           
    @param mu_new: matrix containing membership of each data point to a cluster center
    @return: number of cluster centers and an array which will indicate the number of data points belonging to each cluster point
    @todo:
    pts2clstr = array([[0,0,1,0,1],[1,0,0,0,0],[0,1,0,1,0]]) . It assigns the data points to cluster centers. 
                data points having max membership w.r.t to a cluster center is assigned to that particular cluster center
        
    """
    numCP = mu_new.shape[0]#number of clusters
    num_data_pts = mu_new.shape[1]#number of data points
    #Defining an array which will indicate the number of data points belonging to each cluster point
    pts2clstr = numpy.zeros((numCP,num_data_pts))

    #Checking which cluster point the data point belongs to
    for j in range(num_data_pts):
        max_membership = mu_new[0][j]
        index = 0
        for i in range(1,numCP):
            if mu_new[i][j] > max_membership :
                max_membership  = mu_new[i][j]
                index = i
        pts2clstr[index][j] = 1        
    return numCP,pts2clstr


def reassigning_indices_order(pts2clstr):
    """
     make a list of indices of cluster centers in ascending order based on the number of points that belong to each cluster center
     
    @param pts2clstr: an array which will indicate the number of data points belonging to each cluster point
    @return : list of indices of cluster centers in ascending order by number of points that belong to each cluster centers
    @todo:
    """
    count_list = []
    for row in pts2clstr:
        count_list.append(sum(row))
    copy_count_list = copy.deepcopy(count_list)
    reassigning_list = []
    iteration_count = len(count_list)
    for i in range(iteration_count):
        index = count_list.index(min(copy_count_list))
        reassigning_list.append(index)
        copy_count_list.remove(count_list[index])        
    return reassigning_list


def reassigning_cluster(cluster_centers,key,input_data,q):
    """
    Each data point belonging to a discarded cluster point is reallocated to the cluster point closest to it
    
    @param cluster_centers : array of cluster centers returned by fuzzy_c_means function
    @param key : index of a cluster center in cluster_centers
    @param input_data :array with input data points
    @param q : fuzzifier value
    @return :  membership matrix and cluster centers afrter reallocation
    @todo:  
      
    """  
    #Reallocating data points of discarded cluster points
    #Criteria Used: Each data point belonging to a discarded cluster point is reallocated to the cluster point closest to it
    cluster_centers_copy = copy.deepcopy(cluster_centers)
    num_cluster_centers = int(cluster_centers_copy.shape[0]) - 1
    data_array = copy.deepcopy(input_data)
    num_data_pts = data_array.shape[0]
    cluster_centers_copy = numpy.delete(cluster_centers_copy,key,axis=0)
    distance_matrix = compute_distance_matrix(data_array,cluster_centers_copy)
    mu_new = compute_membership_matrix(distance_matrix,q) 
    return (mu_new,cluster_centers_copy)

def fcm_objective_function_value(membership_matrix, distance_matrix, fuzzifier):
    (num_clusters, num_data_points) = membership_matrix.shape
    objective_fn_value1 = 0.0
    objective_fn_value2 = 0.0
    objective_fn_value3 = 0.0
    for i in range(num_clusters):
        val3=0.0
        for j in range(num_data_points):
            mu_i_j = membership_matrix[i][j]
            d_i_j = distance_matrix[i][j]
            val1 = (mu_i_j ** fuzzifier) * (d_i_j ** 2)
            objective_fn_value1 += val1
            val3 += math.pow(d_i_j,-2)
        objective_fn_value3 += 1/val3
    for i in range(num_data_points):
        val2=0.0
        for j in range(num_clusters):
            mu_i_j = membership_matrix[j][i]
            d_i_j = distance_matrix[j][i]
            val2 += math.pow(d_i_j,-2)
        objective_fn_value2 += 1/val2
    Mu=numpy.zeros((1,num_clusters))
    for i in range(num_clusters):
        val=0.0
        for j in range(num_data_points):
            d_i_j = distance_matrix[i][j]
            val += math.pow(d_i_j,-2)
        Mu[0][i]=val/num_data_points
    return num_clusters*objective_fn_value1/num_data_points, objective_fn_value2, num_data_points*objective_fn_value3/num_clusters, Mu
    
def test_gd_index(membership_matrix):
    (num_clusters, num_data_points) = membership_matrix.shape
    mu_max = 0.0
    mu_min = 0.0
    for i in range(num_data_points):
        mu_max+=numpy.max(membership_matrix[:,i])
        mu_min+=numpy.min(membership_matrix[:,i])
    gd_index = (mu_max-mu_min-num_clusters)/num_data_points
    return gd_index, (mu_max-mu_min)/num_data_points
    
def manoj_index(distance_matrix_between_clusters, fuzzifier):
    num_clusters = distance_matrix_between_clusters.shape[0]
    if num_clusters==1:
        return 1
    else:
        val=0.0
        for i in range(num_clusters):
            for j in range(i):
                if j<i:
                    d_i_j = distance_matrix_between_clusters[i][j]
                    val += math.pow(d_i_j, 2/(1-fuzzifier))
        objective_fn_value = 1/val
    return objective_fn_value*(math.factorial(num_clusters)/((math.factorial(num_clusters-2))*2))

def chi_squared_test(cluster1, cluster2):
    clust1 = numpy.array(cluster1)
    clust2 = numpy.array(cluster2)
    S1 = numpy.matrix(numpy.cov(clust1.T))
    S2 = numpy.matrix(numpy.cov(clust2.T))
    m1 = numpy.matrix(numpy.mean(clust1, axis = 0))
    m2 = numpy.matrix(numpy.mean(clust2, axis = 0))
    stat = (m1-m2)*(numpy.linalg.inv(S1+S2))*(m1-m2).T
    print stat
    return stat
 
if __name__=='__main__':
    path="/home/manu/Documents/Datasets/2clusters_f.tab"
    data_matrix = load_into_file(path)
    data_matrix=numpy.array(data_matrix)
    num_cluster_centers = 2
    Result=numpy.zeros((num_cluster_centers,2))
    
    
    reassigning_flag = 1
    fuzzifier=2
    num_of_data_points = data_matrix.shape[0]
    dim = data_matrix.shape[1]
    J2=0
    for i in range(1):
        cluster_centers_new , membership_matrix = fuzzy_c_means(data_matrix,num_cluster_centers,q=2,tol=.0001)
        if reassigning_flag:
            cluster_centers , membership_matrix = perform_reassigning(cluster_centers_new,membership_matrix,data_matrix,q=2,factor=1.5)
            distance_matrix = compute_distance_matrix(data_matrix,cluster_centers)
            J1, J2, J3, Mu=fcm_objective_function_value(membership_matrix, distance_matrix, fuzzifier)
            if i==0:
                temp = J2
            if J2<=temp:
                cluster_centers_final = cluster_centers
                membership_matrix_final = membership_matrix
                distance_matrix_final = distance_matrix
                temp=J2
    J2=temp
    cluster1=[]
    cluster2=[]
    for i in range(num_of_data_points):
        dist1 = numpy.linalg.norm([cluster_centers[0] - data_matrix[i]])
        dist2 = numpy.linalg.norm([cluster_centers[1] - data_matrix[i]])
        if dist1<=dist2:
            cluster1.append(data_matrix[i])
        else:
            cluster2.append(data_matrix[i])
    print len(cluster1), len(cluster2)
    stat = chi_squared_test(cluster1, cluster2)
    print stat
    
# if __name__=='__main__':
#     path="/home/manu/Documents/Datasets/4clusters_c.tab"
#     data_matrix = load_into_file(path)
#     data_matrix=numpy.array(data_matrix)
#     num_iter=7
#     Result=numpy.zeros((num_iter,2))
#     for iter in range(num_iter):
#         num_cluster_centers = iter+1
#         reassigning_flag = 1
#         fuzzifier=2
#         num_of_data_points = data_matrix.shape[0]
#         dim = data_matrix.shape[1]
#         J2=0
#         for i in range(1):
#             cluster_centers_new , membership_matrix = fuzzy_c_means(data_matrix,num_cluster_centers,q=2,tol=.0001)
#             if reassigning_flag:
#                 cluster_centers , membership_matrix = perform_reassigning(cluster_centers_new,membership_matrix,data_matrix,q=2,factor=1.5)
#                 distance_matrix = compute_distance_matrix(data_matrix,cluster_centers)
#                 J1, J2, J3, Mu=fcm_objective_function_value(membership_matrix, distance_matrix, fuzzifier)
#                 if i==0:
#                     temp = J2
#                 if J2<=temp:
#                     cluster_centers_final = cluster_centers
#                     membership_matrix_final = membership_matrix
#                     distance_matrix_final = distance_matrix
#                     temp=J2
#         J2=temp
#         distance_matrix_between_clusters = compute_distance_matrix(cluster_centers_final,cluster_centers_final)
#         print(J2/manoj_index(distance_matrix_between_clusters, fuzzifier), J2, manoj_index(distance_matrix_between_clusters, fuzzifier))
# # #         J1, J2, J3, Mu=fcm_objective_function_value(membership_matrix_final, distance_matrix_final, fuzzifier)
# # #         J4, J5 = test_gd_index(membership_matrix_final)
# #         J6=manoj_index(distance_matrix_between_clusters, fuzzifier)
# # #         print J1, J2, J3
# # #         print"GD Index"
# # #         print J4, J5, J4-J5
# #         print J2, J6, J6/J2
# #         print "test_new_index", fisher_index(data_matrix, cluster_centers)
# #         Result[iter][0]=num_cluster_centers
# #         Result[iter][1] =J6
# #     pyplot.plot(Result[:,0],Result[:,1])
# #     pyplot.show()