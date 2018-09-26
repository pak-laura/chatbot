

from bs4 import BeautifulSoup
import urllib.request
import re
import requests

def mainUrl():
    starter_url = "https://www.britannica.com/place/Turkey"
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    mainUrls = set()
    urlCount = 0
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if 'Turkey' in link_str or 'turkey' in link_str:
            if 'turkey-bird' not in link_str:
                #if the string is from same domain and does not include #--will not get copies of same page
                if link_str.startswith("/") and "#" not in link_str and len(mainUrls) < 15:
                    mainUrls.add(starter_url + str(link.get('href')))
                if link_str.startswith("https:") and urlCount < 7 and len(mainUrls) < 15:
                    urlCount += 1
                    mainUrls.add(str(link.get('href')))
                
    print (mainUrls)
    print(len(mainUrls))
    print("end of crawler")
    return(mainUrls)

def visible(element):
   if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
      return False
   elif re.match('<!--.*-->', str(element.encode('utf-8'))):
   # elif re.match('<!--.*-->'.encode('utf-8'), element.encode('utf-8')):
      return False
   return True

# scrape text from list of urls
def scrapeUrls(links):
   fileNames = []
   for ind, url in enumerate(links):
      html = urllib.request.urlopen(url)
      soup = BeautifulSoup(html, 'lxml')
      data = soup.findAll(text = True)
      textIter = filter(visible, data)
      urlText = ' '.join(list(textIter))
      with open(str(ind)+'_in', 'w') as writeFile:
         writeFile.write(str(urlText.encode('utf-8')))
      fileNames.append(str(ind)+'_in')
   return fileNames

# func to clean text
def cleanText(files):
   # loop inside file to prevent calling again & again
   for ind, f in enumerate(files):
      currFile = open(f, 'r')
      fileString = currFile.read().replace('\n', ' ')
      with open(str(ind)+'_out', 'w') as writeFile:
         writeFile.write(fileString)


def main():
   #return list of 15 relevant urls
   mainUrls = mainUrl()
   filesIn = scrapeUrls(mainUrls)
   cleanText(filesIn)

if __name__ == '__main__':
    main()
