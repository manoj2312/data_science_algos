from cvxopt import matrix
from cvxopt.glpk import ilp
import copy
import json
import numpy
import random


# # The following function computes the required constraint matrices for the case where number of autos is less than the number of customers
def parseJsonText(inDict):
    dataMatrix = []
    n = len(inDict["origin_addresses"])
    c = len(inDict["destination_addresses"])
    for rowIndex, rowDict in enumerate(inDict["rows"]):
        for colIndex, colDict in enumerate(rowDict["elements"]):
            info = {"from_place" : inDict["destination_addresses"][rowIndex],
                    "to_place" : inDict["origin_addresses"][colIndex],
                    "distance" : colDict["distance"]["value"],
                    "time" : colDict["duration"]["value"]}
            dataMatrix.append(info)
    distance = []
    time = []
    for line in dataMatrix:
        distance.append(line["distance"])
        time.append(line["time"])
    distance = numpy.reshape(numpy.array(distance), (n, c))
    time = numpy.reshape(numpy.array(time), (n, c))
    return distance, time, n, c

def prepare_I_and_B_matrices(func):
    def _inner(*args, **kwargs):
        numAutos = args[0]
        numCust = args[1]
        I = set()
        B = set(range(numAutos * numCust))
        G, h, A, b = func(*args, **kwargs)
        return G, h, A, b, I, B
    return _inner
    

@prepare_I_and_B_matrices
def allAutoAssignment(numAutos, numCust):
    G = matrix(0, (numCust, numAutos * numCust), 'd')
    for i in range(numCust):
        G[i, range(i, numAutos * numCust, numCust)] = 1
    h = matrix(1, (numCust, 1), 'd')
    A = matrix(0, (numAutos, numAutos * numCust), 'd')
    for i in range(numAutos):    
        A[i, (i * numCust):(i + 1) * numCust] = 1
    b = matrix(1, (numAutos, 1), 'd')
    return G, h, A, b

'The following function computes the required constraint matrices for the case where number of customers is less than the number of autos'

@prepare_I_and_B_matrices
def allCustAssignment(numAutos, numCust):
    G = matrix(0, (numAutos, numAutos * numCust), 'd')
    for i in range(numAutos):
        G[i, (i * numCust):(i + 1) * numCust] = 1
    h = matrix(1, (numAutos, 1), 'd')
    A = matrix(0, (numCust, numAutos * numCust), 'd')
    for i in range(numCust):
        A[i, range(i, numAutos * numCust, numCust)] = 1    
    b = matrix(1, (numCust, 1), 'd')
    return G, h, A, b
'The following function computes the required constraint matrices for the case where number of autos is equal to the number of customers'

@prepare_I_and_B_matrices
def allAutoCustAssignment(numAutos, numCust):
    G = matrix(0, (numAutos + numCust, numAutos * numCust), 'd')
    h = matrix(0, (numAutos + numCust, 1), 'd')
    A = matrix(0, (numAutos + numCust, numAutos * numCust), 'd')
    for i in range(numAutos):
        A[i, (i * numCust):(i + 1) * numCust] = 1
    for i in range(numCust):
        A[numAutos + i, range(i, numAutos * numCust, numAutos)] = 1
    b = matrix(1, (numAutos + numCust, 1), 'd')
    return G, h, A, b
     
def entryPointForJ2(dataRead):
    finalResult = main(dataRead)
    return finalResult

def optimization(distanceMatrix, numAutos, numCust):
    distanceMatrix = numpy.array(distanceMatrix)
    c = numpy.ones((numAutos * numCust, 1))
    count = 0
    for i in range(numAutos):
        for j in range(numCust):
            c[count][0] = distanceMatrix[i][j]
            count = count + 1
    if numAutos < numCust:
        G, h, A, b, I, B = allAutoAssignment(numAutos, numCust)
    elif numAutos > numCust:
        G, h, A, b, I, B = allCustAssignment(numAutos, numCust)
    else:
        G, h, A, b, I, B = allAutoCustAssignment(numAutos, numCust)
    (status, x) = ilp(c, G, h, A, b, I, B)
    return x, numAutos, numCust

def assignmentResults(solution, num_autos, num_customers):
    dictResults=[]
    for i in range(len(solution)):
        if solution[i] == 1.0:
            tempDict={'Auto':[], 'Customer': []}
            tempDict['Auto'] = i / num_customers + 1
            tempDict['Customer'] = i % num_customers + 1
#             print "Auto Number", i / num_customers + 1, "is going to the customer number", i % num_customers + 1
            dictResults.append(tempDict)
    jsonResults=json.dumps(dictResults)
    return jsonResults

def main(dataRead):
    dataRead_dict = json.loads(dataRead)
    distanceMatrix, timeMatrix, numAutos, numCust = parseJsonText(dataRead_dict)
    distanceMatrix =numpy.random.random((10,10))
    x, numAutos, numCust = optimization(distanceMatrix, 10,10)
    dictResults = assignmentResults(x, numAutos, numCust)
    return dictResults

# # def greedyAlgorithm(distMat):
# distMat=[[5,4,1,2],[2,3,4,1]]
# temp=copy.deepcopy(distMat)
# distMat=numpy.array(distMat)
# index=numpy.zeros((min(distMat.shape[0],distMat.shape[1])))
# m=0
# while True:
#     if min(distMat.shape[0],distMat.shape[1])==0:
#         break
#     else:
#         index[m] = numpy.argmin(distMat)
#         row = int(index[m]//distMat.shape[1])
#         col = int(index[m]%distMat.shape[1])
#         print row, col, 'hii'
#         rowCount=0
#         colCount=0
#         mat=numpy.zeros((distMat.shape[0]-1,distMat.shape[1]-1))
#         print distMat.shape 
#         for i in range(distMat.shape[0]):
#             for j in range(distMat.shape[1]):
#                 print i,j,'hey', row, col
#                 print (i==row) or (j==col)
#                 if (i==row) or (j==col):
#                     print 'deleted this term'
#                 else:
#                     print i, j, "i,j"
#                     mat[rowCount][colCount]=distMat[i][j]
#                     colCount+=1
#             rowCount+=1
#         distMat=mat
#         m=m+1
# print index
# print temp