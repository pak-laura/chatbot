

from bs4 import BeautifulSoup
import urllib.request
import re
import requests
from urllib.request import Request, urlopen

def visible(element):
   if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
      return False
   elif re.match('<!--.*-->', str(element.encode('utf-8'))):
   # elif re.match('<!--.*-->'.encode('utf-8'), element.encode('utf-8')):
      return False
   return True

'''url = 'https://www.congress.gov/congressional-record/2018/9/18/senate-section/article/S6210-2'
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'lxml')
data = soup.findAll(text = True)
textIter = filter(visible, data)
urlText = ' '.join(list(textIter))
with open('fileToSave', 'w') as writeFile:
   print(url)
   print(urlText.encode('utf-8'))
   writeFile.write(str(urlText.encode('utf-8')))
'''
req = Request('https://www.congress.gov/congressional-record/2018/9/18/senate-section/article/S6210-2', headers = {'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
print(webpage)