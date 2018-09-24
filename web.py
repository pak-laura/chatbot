# ??

from bs4 import BeautifulSoup
import urllib.request
import re
import requests


# starter_url = "https://travel.usnews.com/rankings/worlds-best-vacations/"
starter_url = "https://www.britannica.com/place/Turkey"
# starter_url = "https://travel.state.gov/content/travel/en/international-travel/International-Travel-Country-Information-Pages/Turkey.html"
r = requests.get(starter_url)

data = r.text
soup = BeautifulSoup(data, "lxml")


# write urls to a file
with open('urls.txt', 'w') as f:
   for link in soup.find_all('a'):
      link_str = str(link.get('href'))
      if 'Turkey' in link_str:
         f.write(str(link.get('href')) + '\n\n')

# end of program
print("end of crawler")

def visible(element):
   if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
      return False
   elif re.match('<!--.*-->', str(element.encode('utf-8'))):
   # elif re.match('<!--.*-->'.encode('utf-8'), element.encode('utf-8')):
      return False
   return True

def scrapeUrls(links):
   for ind, url in enumerate(links):
      html = urllib.request.urlopen(url)
      soup = BeautifulSoup(html, 'lxml')
      data = soup.findAll(text = True)
      textIter = filter(visible, data)
      urlText = ' '.join(list(textIter))
      with open(ind, 'w') as writeFile:
         print(url)
         print(urlText.encode('utf-8'))
         writeFile.write(str(urlText.encode('utf-8')))

with open('myurls.txt', 'r') as linksFile:
   mylist = [re.sub('\n','',line) for line in linksFile]
   print(mylist)
   scrapeUrls(mylist)