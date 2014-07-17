'''
Created on Jul 7, 2014

@author: manu
'''

# code to form a list of all working dates from 2000 to 2014
# 'year' -> the start year. 'month' -> the start month. 'day' -> the start day.
#------------------------------------------------------------ year = sys.argv[1]
#----------------------------------------------------------- month = sys.argv[2]
#------------------------------------------------------------- day = sys.argv[3]
#------------------------------------------------------------ iter = sys.argv[4]

year = 2000 
month = 1
day = 2
iter = 753

date=[]

def feb(yr):
    if((yr%4)==0):
        return 29
    else:
        return 28
          
def monthlist(yr):
    return [31,feb(yr),31,30,31,30,31,31,30,31,30,31]
   
def mop(num):
    if(num<10):
        return '0'+str(num) 
    else:
        return str(num)
       
def dator(yr,mn,dy):
    return str(yr) + '-' + mop(mn) + '-' + mop(dy)
       
       
for j in range(iter):
    for i in range(5):
        if(day<monthlist(year)[month]):
            day=day+1
            date.append( dator(year,month+1,day) ) 
        elif( (day>=monthlist(year)[month]) & (month<11) ):
            day=day-monthlist(year)[month] + 1
            month=month+1
            date.append( dator(year,month+1,day) )
        else:
            day=day-monthlist(year)[month] + 1
            month=0
            year=year+1
            date.append( dator(year,month+1,day) )
    day=day+2        
   
 
print date
