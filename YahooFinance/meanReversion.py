import os
import csv
import xlrd
import xlwt
import traceback
import datetime

def readRows(path, name):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    style = xlwt.XFStyle()
    style.num_format_str = 'DD-MM-YYYY'
    workbook = xlrd.open_workbook(str(path))
    worksheet = workbook.sheet_by_index(0)
    for i in range(worksheet.nrows):
        if i ==43351 :
            print "I am skipping from this line "
            break
        if i!=0:
            row = str(worksheet.row(i)[5])
            date = datetime.datetime(*xlrd.xldate_as_tuple(worksheet.cell_value(rowx=i, colx=0), workbook.datemode))
            sheet1.write(i-1, 0, date, style)
            sheet1.write(i-1, 1, float(row.split(':')[1]))
    
    os.chdir('/home/manu/Documents/MeanReversion/Stage2/FINAL DATA/FormattedData')
    book.save(str(name.split('.')[0])+'.xls')
    return book

os.chdir('/home/manu/Documents/MeanReversion/Stage2/FINAL DATA/FormattedData')
completed_files = [f for f in os.listdir('.') if os.path.isfile(f)]
completed_files_converting_xlsx = [str(f)+"x" for f in completed_files]

os.chdir('/home/manu/Documents/MeanReversion/Stage2/FINAL DATA')
print os.listdir('/home/manu/Documents/MeanReversion/Stage2/FINAL DATA')

files = [f for f in os.listdir('.') if os.path.isfile(f) and f not in completed_files_converting_xlsx]
print "Number of files i will convert are "
print len(files)
count=0
for f in files:
    try:
        count+=1
        print count, str(f)
        path='/home/manu/Documents/MeanReversion/Stage2/FINAL DATA/'+str(f)
        Book = readRows(path, str(f))
    except Exception:
        print str(f)
        print traceback.format_exc()
        continue
    