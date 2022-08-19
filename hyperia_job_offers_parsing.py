from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.hyperia.sk'

req = requests.get(url + '/kariera/')
req.encoding = 'UTF-8'
content = req.text

soup = BeautifulSoup(content, 'html.parser')

titles, hrefs, places, salaries, types, emails = [], [], [], [], [], []
jsonData = []

titles = soup.find(id="positions").find_all('h3')
hrefs = soup.find(id="positions").find_all('a')

for href in hrefs:
    
    req = requests.get(url + href['href'])
    req.encoding = 'UTF-8'
    content = req.text
    soup = BeautifulSoup(content, 'html.parser')
    data = soup.find_all(class_='col-md-4 icon')
    
    places.append(str(data[0].get_text()).split(':')[1])
    salaries.append(str(data[1].get_text()).split('ohodnotenie')[1])
    types.append(str(data[2].get_text()).split('pomeru')[1])
    emails.append(soup.find(class_='container position-contact').find('strong').get_text())
    

for i in range(0, len(titles)):
    
    part = {}

    part["title"] = titles[i].get_text()
    part["place"] = places[i]
    part["salary"] = salaries[i]
    part["type"] = types[i]
    part["email"] = emails[i]

    jsonData.append(part)
    

with open("output.json", "w", encoding='utf-8') as write_file:
    json.dump(jsonData, write_file, indent=5, ensure_ascii=False)

 
