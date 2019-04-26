import requests
import functions as func
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
cookies = dict(SID='UQfgNZmamqHhoMVyF5m7ZbKxtBXR13_OIN3wA0FPoH_M4iCgbFj_TyzhQJCtx_d39x2W5g.')
response = requests.get('https://www.google.com/search?num=100&q=site:' + input('Insert domain (without http(s)://):'),
                        headers=headers,
                        cookies=cookies
                        )

if response.status_code == 200:

    links = []

    print('Parsing the links...')
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all('div', {'class': 'r'})
    navigation = soup.find('div', {'id': 'navcnt'}).find_all('a', {'class': 'fl'})

    # total = soup.find('div', {'id': 'resultStats'}).text
    # total = int(re.sub('\\D', '', re.sub('\\(.*\\)', '', total)))

    links += func.extractor(items)

    # if total > 100:
    for nav in navigation:
        href = nav.get('href')
        response = requests.get('https://www.google.com' + href, headers=headers, cookies=cookies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all('div', {'class': 'r'})
            links += func.extractor(items)
            time.sleep(5)
        else:
            print('eCaptcha found in nav links')
            raise SystemExit(1)
    print('Found: ' + str(len(links)) + ' links')

else:
    print('Bad URL or reCaptcha found! Try later')
    raise SystemExit(1)

print('Checking...')

i = 0
f = open('results-' + str(datetime.today().strftime("%Y-%m-%d_%H-%M-%S")) + '.txt', 'w')
for item in links:
    response = requests.get(item)
    if response.status_code != 200:
        # print(item + ' response code not 200!')
        f.write(item + ' response code not 200!' + '\n')
        i += 1
f.close()

print('Check was complete, found ' + str(i) + ' bad links')
