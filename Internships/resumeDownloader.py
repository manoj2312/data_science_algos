import socket
import urllib
from urllib import request, error
import copy
import numpy
import xlrd
from bs4 import BeautifulSoup
import traceback
from traceback import format_exc
socket.timeout(10000000)

def pingUrl(url):
    html=[]
    try :
        response = urllib.request.urlopen(url) 
        html = response.read()
    except Exception:
        print(traceback.format_exc())
    else :
        html = response.read()
        print('got response!')
    return html


url='http://www.google.com/search?as_q=nintendo&as_eq=wii&as_sitesearch=.com'
data = pingUrl(url)
print(len(data))



# soup = BeautifulSoup()
# 
# for a in soup.find_all('a', href=True):
#     print("Found the URL:", a['href'])