import requests
from bs4 import BeautifulSoup
import csv
import re

# Finding TVs:
def FindTVbyAdderess(url):
    # list of links
    linkList = GenerateLinksList(url)
    # words in each page
    resdict = {}
    # page number
    page = 0
    # words organized by pages
    pageList = []
    for link in linkList:
        page += 1
        source_code = requests.get(link)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for y in soup.findAll('ul'):
            x = y.select("div")
            # search for tvs that their address is - נצרת עילית
            if x.__len__() > 3 and x[3].string and x[3].string.__contains__("כתובת"):
                add = x[3].string.replace('כתובת:', "")
                if add.__contains__("נצרת עילית"):
                    soup2 = BeautifulSoup(plain_text, 'html.parser')
                    # extract words from the title
                    tvs = soup2.find_all('span', {'class': "breadcrumb-item active"})
                    listOnWords = tvs[0].string.replace("\n", "").split(" ")
                    for word in listOnWords:
                        if word != '':
                            if word in resdict:
                                resdict[word] = resdict[word] + 1
                            else:
                                resdict.update({word: 1})
                    # extract words from the description
                    tvs = soup2.find_all('div', {'class': "text-content"})
                    listOnWords = tvs[0].string.replace("\n", "").split(" ")
                    for word in listOnWords:
                        if word != '' and not word.__contains__("\u200b"):
                            if word in resdict:
                                resdict[word] = resdict[word] + 1
                            else:
                                resdict.update({word: 1})
                    tvs = soup2.find_all('div', {'class': "product-title show-mobile"})
                    listOnWords = tvs[0].string.replace("\n", "").split(" ")
                    for word in listOnWords:
                        if word != '':
                            if word in resdict:
                                resdict[word] = resdict[word] + 1
                            else:
                                resdict.update({word: 1})
        # update the page list
        if resdict != {}:
            pageList.append([page, resdict.copy()])
            resdict = {}
    # print result
    with open('addresses.csv', 'w') as csv_file:
        headers = ["Word", "Counter", "Page"]
        writer = csv.writer(csv_file)
        writer.writerow(i for i in headers)
        for record in pageList:
            for key, value in record[1].items():
                writer.writerow([key, value, record[0]])


def GenerateLinksList(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    linkList = []
    for link in soup.findAll('a', attrs={'href': re.compile("/deal/")}):
        linkList.append(url + link.get('href'))
    return linkList


FindTVbyAdderess('https://www.groo.co.il/category/304/tv/')


