# ??

from bs4 import BeautifulSoup
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
         print(link.get('href'))
         f.write(str(link.get('href')) + '\n\n')

# end of program
print("end of crawler")
