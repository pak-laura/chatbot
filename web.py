# Names: Maliha Haque and Laura Pak
# Date: 9/30/18
# Assignment: Webcrwaler- Project Part 1
# Class: CS 4301: Introduction to Natural Language Processing


from bs4 import BeautifulSoup
import urllib.request
import re
import requests
import nltk
from nltk import sent_tokenize, word_tokenize, FreqDist
from nltk.corpus import stopwords
import string

#starter url and get 15 relvant urls
def mainUrl():
    starter_url = "https://www.britannica.com/place/Turkey"
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    mainUrls = set()
    urlCount = 0
    
    #get 15 relevant urls
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


# clean text
def cleanText(files):
   tokensAll = []
   sents = []
   # loop inside file to prevent calling again & again
   for ind, f in enumerate(files):
      currFile = open(f, 'r')
      fileString = currFile.read().replace('\\n', '')
      fileString = fileString.replace('\\t', '')
      fileString = fileString.replace('\\r', '')
      fileString = re.sub(r'\s', ' ', fileString)
      fileString = re.sub('[^A-Za-z\.]+', ' ', fileString.lower())
      sents += nltk.sent_tokenize(fileString)
      fileString = re.sub('[^A-Za-z]+', ' ', fileString.lower())
      #print(fileString[:500])
      #print('-----------------------------')
      #print('-----------------------------')
      #print('-----------------------------')
      tokens = word_tokenize(fileString)
      #print("tokens after tokenizing: ", tokens)
      tokensAll += [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
      with open(str(ind)+'_out', 'w') as writeFile:
         writeFile.write(' '.join(sents))
   return tokensAll, sents


# find top terms and build knowledge base
def topTerms(tokens, sents):
    
    badWords = ['x', 'xc', 'xbcrk', 'xe', 'xa', 'xb', 'dia', 'p', 'britannica']
    termDict = {}
    tokens = [word for word in tokens if word not in badWords]
    lenght = len(set(tokens))
    cleanSents = []
    for sent in sents:
        s = word_tokenize(sent)
        e = [w for w in s if w not in badWords]
        sent = ' '.join(e)
        cleanSents.append(sent)

    #find fdist for words to get most common terms
    fdist = FreqDist(tokens)
    print(fdist.most_common(40))
    for i,p in fdist.most_common(lenght):
        termDict[i] = p

    #build knowledge base with top terms
    topTerms = ['turkey', 'history', 'population', 'istanbul', 'people', 'life', 'arts', 'education', 'government', 'social'] 
    with open('knowledge_base', 'w+') as writeFile:
        for term in topTerms:
            for sent in cleanSents:
                if term in sent:
                        writeFile.write(term + "-- " + sent + "\n")



def main():
   #return list of 15 relevant urls
   mainUrls = mainUrl()

   #scrape urls for text
   filesIn = scrapeUrls(mainUrls)

   #clean text
   tokens, sents = cleanText(filesIn)

   #get top terms and print knowledge base to file
   topTerms(tokens, sents)
  
if __name__ == '__main__':
    main()
