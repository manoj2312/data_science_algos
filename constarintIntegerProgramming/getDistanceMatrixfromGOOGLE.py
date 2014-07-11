import socket
import urllib
from intProgCode import main
import copy
import numpy
import time

socket.setdefaulttimeout(100000)  # timeout in seconds
def load_into_file(path,header=True):
    File=open(path,'r')
    lines=File.readlines()
    final_list=[]
    for line in lines:
            final_list.append([float(i) for i in line.split(',')])
    File.close()
    return final_list

def constructURL(origins,destinations):
    key="AIzaSyAZfJdA7q9lszsjiqfuOk_DlXG1MvZsqr0"
    baseURL="https://maps.googleapis.com/maps/api/distancematrix/json?"
    mode="driving"
    language="en-US"
    sensor="false"
    url=baseURL+"origins="+origins+"&destinations="+destinations+"&mode="+mode+"&language="+language+"&sensor="+sensor+"&key="+key
    return url

def pingUrl(url):
    Count=1
    dataRead=[]
    while Count<10:
        try :
            response = urllib.request.urlopen( url )
            dataRead = response.read()
        except urllib.error.HTTPError, e:
            print 'The server couldn\'t fulfill the request. Reason:', str(e.code)
            Count=copy.deepcopy(Count+1)
        except urllib.error.URLError, e:
            print 'We failed to reach a server. Reason:', str(e.reason)
            Count=copy.deepcopy(Count+1)
        else :
            html = response.read()
            Count=11
#             print 'got response!'
    return dataRead

def originsAndDestinations():
    pathForAutoData="/home/manu/Documents/IntegerLinearProgramming/autoCood.txt"
    pathForCustData="/home/manu/Documents/IntegerLinearProgramming/customerCood.txt"
    autoCood=numpy.array(load_into_file(pathForAutoData))
    custCood=numpy.array(load_into_file(pathForCustData))

    autoString= ""
    for i in range(autoCood.shape[0]):
        autoString += "%f,%f"%(custCood[i][0],autoCood[i][1])
        if i<autoCood.shape[0]-1:
            autoString += "|"
    custString= ""
    for i in range(custCood.shape[0]):
        custString += "%f,%f"%(custCood[i][0],custCood[i][1])
        if i<custCood.shape[0]-1:
            custString += "|"
    return autoString, custString

def parseJsonforJ1(jsonCoordinates):
    auto=jsonCoordinates["autoLocation"]
    cust=jsonCoordinates["customerLocation"]
    autoCood=[]
    custCood=[]
    for i in range(len(auto)):
        temp = []
        temp.append(auto[i].get('latitude'))
        temp.append(auto[i].get('longitude'))
#         temp.append(auto[i].get('name'))
        autoCood.append(temp)
    autoCood=numpy.array(autoCood)
    autoString= ""
    for i in range(autoCood.shape[0]):
        autoString += "%f,%f"%(float(autoCood[i][0]),float(autoCood[i][1]))
        if i<autoCood.shape[0]-1:
            autoString += "|"
    for i in range(len(cust)):
        temp = []
        temp.append(cust[i].get('latitude'))
        temp.append(cust[i].get('longitude'))
        custCood.append(temp)
    custCood=numpy.array(custCood)
    custString= ""
    for i in range(custCood.shape[0]):
        custString += "%f,%f"%(float(custCood[i][0]),float(custCood[i][1]))
        if i<custCood.shape[0]-1:
            custString += "|"
    return autoString, custString
 
def entryPointforJ1(jsonCoordinates):
    autoString, custString = parseJsonforJ1(jsonCoordinates)
    url=constructURL(autoString,custString)
    jsonDistMat = pingUrl(url)
    finalResult = main(jsonDistMat)
    return finalResult

if __name__=='__main__':
    tic=time.clock()
    autoString, custString = originsAndDestinations()
    url=constructURL(autoString,custString)
    jsonDistMat = pingUrl(url)
    finalResult = main(jsonDistMat)
    print finalResult
    toc = time.clock()
    print toc-tic