from bs4 import BeautifulSoup
import requests as req
from selenium import webdriver

session = req.Session()
data = {"login_username":"pantimus", "login_password":"Emtpaemtpa."}
url = "http://github.com/login.php"
user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')
url_search = "https://github.com/search?q=vue"

response = session.post(url, data=data)
href_array=[]

def tree(href_array):
    for row in table.findAll('tr')[1:]:
    col = row.findAll('td')

    d = {    
            'tag' : col[0].getText(),
            'component': col[1].getText(),
            'name' : col[2].getText(),
            'framework' : col[3].getText(),
        }

    for key, val in d.items():
        val = val.replace('\n', '')
        val = val.replace(',', '')
        d[key] = val

        try:
            if key not in  ['rank', 'volume']:
                d[key] = float(val)
            else:
                d[key] = int(val)
        except Exception as e:
            pass

    data.append(d)
    return data

for page in range(5):
    url_page = "https://github.com/search?p={}&q=vue&type=Repositories".format(page)
    response = req.get(url_page, timeout=(25, 5), headers={'User-Agent':user_agent}).content
    soup = BeautifulSoup(response, "lxml")
    soup.prettify()
    for link in soup.find_all("div", { "class":"f4 text-normal"}):
        href = [item['href'] for item in link.select('[href]')]
        href_array.append(href[0])
        for repository_access in range(len(href_array)):
            url_repository = "https://github.com/{}".format(repository_access)
            response_repository = req.get(url_repository, timeout=(25, 5), headers={'User-Agent':user_agent}).content
            repository = BeautifulSoup(response_repository, "lxml")
            repository.prettify()
            for link in repository.find_all("a", { "class":"js-navigation-open link-gray-dark"}):
                href = [item['href'] for item in link.select('[href]')]
                href_array.append(href[0])
                answer = tree(href_array)

order=['tag', 'component', 'name', 'framework']                
with open('output.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=order)
    writer.writeheader()
    writer.writerows(answer)