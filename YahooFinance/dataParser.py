import copy
import numpy

def parseData(Count, dataRead):
    Data=[]
    if Count==11:
        dataParsed=[]
        rows=[]
        for row in dataRead.strip().split('\n'):
            for column in row.strip().split(','):
                rows.append(column)
            rowData=copy.deepcopy(rows)
            dataParsed.append(rowData)
            del rows
            rows=[]
        # Header array contains the strings of header of the stock data
        Header=copy.deepcopy(dataParsed[0])  
        del dataParsed[0]
        dataParsed=numpy.array(dataParsed)
        
        Date=[]
        openPrice=[]
        highPrice=[]
        lowPrice=[]
        closePrice=[]
        Volume=[]
        adjClose=[]
        for i in range(dataParsed.shape[0]):
            for j in range(dataParsed.shape[1]):
                if j==0:
                    Date.append(dataParsed[i][j])
                elif j==1:
                    openPrice.append(float(dataParsed[i][j]))
                elif j==2:
                    highPrice.append(float(dataParsed[i][j]))
                elif j==3:
                    lowPrice.append(float(dataParsed[i][j]))
                elif j==4:
                    closePrice.append(float(dataParsed[i][j]))
                elif j==5:
                    Volume.append(float(dataParsed[i][j]))
                elif j==6:
                    adjClose.append(float(dataParsed[i][j]))
        Data=[Header, Date, openPrice, highPrice, lowPrice, closePrice, Volume, adjClose]
    return Count, Date, adjClose
        

def getSymbols(path):
    symbols=[]
    names=[]
    for pathNum in range(len(path)):
        file=open(path[pathNum],'r')
        lines=file.readlines()
        for index,value in enumerate(lines):
            if index%3==0:
                count=copy.deepcopy(0)
                for j in value.strip().split('\t'):
                    if count==0:
                        symbols.append(j)
                        count=copy.deepcopy(1)
                    elif count==1:
                        names.append(j)
                        count=copy.deepcopy(2)
        file.close()
    return symbols,names