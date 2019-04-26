import requests
import functions as func
import time
import re
import sys
import design
from PyQt5 import QtWidgets
from datetime import datetime
from bs4 import BeautifulSoup


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.starButton.clicked.connect(self.start)



    def extractor(self, items):
        links = []
        for item in items:
            link = item.find('a').get('href')
            link = re.sub('&sa=U.*', '', re.sub('/url\\?q=', '', link))
            links.append(link)
        return links

    def start(self):
        text = self.lineEdit.text()
        if text != '':

            self.lineEdit.setDisabled(True)

            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
            cookies = dict(SID='UQfgNZmamqHhoMVyF5m7ZbKxtBXR13_OIN3wA0FPoH_M4iCgbFj_TyzhQJCtx_d39x2W5g.')
            response = requests.get('https://www.google.com/search?num=100&q=site:' + text,
                                    headers=headers,
                                    cookies=cookies
                                    )

            if response.status_code == 200:

                links = []

                self.listWidget.addItem('Parsing the links...')
                soup = BeautifulSoup(response.content, "html.parser")
                items = soup.find_all('div', {'class': 'r'})
                navigation = soup.find('div', {'id': 'navcnt'}).find_all('a', {'class': 'fl'})

                # total = soup.find('div', {'id': 'resultStats'}).text
                # total = int(re.sub('\\D', '', re.sub('\\(.*\\)', '', total)))

                links += self.extractor(items)

                # if total > 100:
                for nav in navigation:
                    href = nav.get('href')
                    response = requests.get('https://www.google.com' + href, headers=headers, cookies=cookies)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")
                        items = soup.find_all('div', {'class': 'r'})
                        links += self.extractor(items)
                        time.sleep(5)
                    else:
                        print('eCaptcha found in nav links')
                        raise SystemExit(1)
                self.listWidget.addItem('Found: ' + str(len(links)) + ' links')

            else:
                self.listWidget.addItem('Bad URL or reCaptcha found! Try later')
                raise SystemExit(1)

            self.listWidget.addItem('Checking...')

            i = 0
            f = open('results-' + str(datetime.today().strftime("%Y-%m-%d_%H-%M-%S")) + '.txt', 'w')
            for item in links:
                response = requests.get(item)
                if response.status_code != 200:
                    # print(item + ' response code not 200!')
                    f.write(item + ' response code not 200!' + '\n')
                    i += 1
            f.close()

            self.listWidget.addItem('Check was complete, found ' + str(i) + ' bad links')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
