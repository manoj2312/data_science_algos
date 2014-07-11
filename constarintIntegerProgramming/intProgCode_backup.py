from cvxopt.glpk import ilp
from cvxopt import matrix
from getDistanceMatrixfromGOOGLE import jsonDistanceMatrix
import numpy
import json

## The following function computes the required constraint matrices for the case where number of autos is less than the number of customers
def parseJsonText(inDict):
    dataMatrix = []
    n=len(inDict["origin_addresses"])
    c=len(inDict["destination_addresses"])
    for rowIndex,rowDict in enumerate(inDict["rows"]):
        for colIndex,colDict in enumerate(rowDict["elements"]):
            info = {"from_place" : inDict["destination_addresses"][rowIndex],
                    "to_place" : inDict["origin_addresses"][colIndex],
                    "distance" : colDict["distance"]["value"],
                    "time" : colDict["duration"]["value"]}
            dataMatrix.append(info)
    distance=[]
    time=[]
    for line in dataMatrix:
        distance.append(line["distance"])
        time.append(line["time"])
    distance=numpy.reshape(numpy.array(distance),(n,c))
    time=numpy.reshape(numpy.array(time),(n,c))
    return distance, time, n, c

def assignmentOptimization(numAutos, numCust):
    if numAutos<numCust:
        G=matrix(0,(numCust,numAutos*numCust),'d')
        for i in range(numCust):
            G[i,range(i,numAutos * numCust,numCust)]=1
        h=matrix(1,(numCust,1),'d')
        A=matrix(0,(numAutos,numAutos*numCust),'d')
        for i in range(numAutos):    
            A[i,(i*numCust):(i+1)*numCust]=1
        b=matrix(1,(numAutos,1),'d')
    elif numAutos>numCust:
        G=matrix(0,(numAutos,numAutos*numCust),'d')
        for i in range(numAutos):
            G[i,(i*numCust):(i+1)*numCust]=1
        h=matrix(1,(numAutos,1),'d')
        A=matrix(0,(numCust,numAutos*numCust),'d')
        for i in range(numCust):
            A[i,range(i,numAutos * numCust,numCust)]=1    
        b=matrix(1,(numCust,1),'d')
    else:
        G=matrix(0,(numAutos+numCust,numAutos*numCust),'d')
        h=matrix(0,(numAutos+numCust,1),'d')
        A=matrix(0,(numAutos+numCust,numAutos*numCust),'d')
        for i in range(numAutos):
            A[i,(i*numCust):(i+1)*numCust]=1
        for i in range(numCust):
            A[numAutos+i,range(i,numAutos * numCust,numAutos)]=1
        b=matrix(1,(numAutos+numCust,1),'d')
    I = set()
    B = set(range(numAutos * numCust))
    return G,h,A,b,I,B

## The following function only prints the results in an easily interpretable way
def print_my_soln(status,solution, num_autos,num_customers):
    print "The optimization solution is", status
    for i in range(len(solution)):
        if solution[i]==1.0:
            print "Auto Number",i/num_customers + 1, "is going to the customer number",i%num_customers + 1
#             print "Auto Driver at the place", origins[0][i/num_customers], "should go to the customer at the place", destinations[0][i%num_customers]
## This is where the code execution starts          

dataRead=jsonDistanceMatrix() ## dataRead is the json sent by the google maps

dataRead_dict = json.loads(dataRead)
distanceMatrix, timeMatrix, numAutos, numCust = parseJsonText(dataRead_dict)
distanceMatrix=numpy.array(timeMatrix)
c=numpy.ones((numAutos*numCust,1))
count=0
for i in range(numAutos):
    for j in range(numCust):
        c[count][0]=distanceMatrix[i][j]
        count=count+1

G, h, A, b, I, B = assignmentOptimization(numAutos, numCust)

(status, x) = ilp(c, G, h, A, b, I, B)
print "Number of Autos is", numAutos
print "Number of Customers is",numCust
print_my_soln(status, x, numAutos, numCust)