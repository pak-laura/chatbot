

from bs4 import BeautifulSoup
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



def main():

    #return list of 15 relevant urls
    mainUrls = mainUrl()


if __name__ == '__main__':
    main()