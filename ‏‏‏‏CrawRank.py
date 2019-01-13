import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import csv
import re

# Finding restorants  :
def FindRestorants(url):
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
        for rank in soup.findAll('div', {'class': "detail bar-detail"}):
            if rank.__str__().__contains__("נקנו"):
                buyCount = rank.find_all('div', {'class': "text"})
                count = buyCount[0].string.replace("נקנו", "")
                count = count.replace("\n", "")
                Rank = float(count.replace("+", ""))
                if Rank > 100:
                    soup2 = BeautifulSoup(plain_text, 'html.parser')
                    restorant = soup2.find_all('span', {'class': "breadcrumb-item active"})
                    listOnWords = restorant[0].string.replace("\n", "").split(" ")
                    for word in listOnWords:
                        if word != '':
                            if word in resdict:
                                resdict[word] = resdict[word] + 1
                            else:
                                resdict.update({word: 1})
                    # extract words from the description
                    restorant = soup2.find_all('div', {'class': "text-content"})
                    listOnWords = restorant[0].string.replace("\n", "").split(" ")
                    for word in listOnWords:
                        if word != '' and not word.__contains__("\u200b"):
                            if word in resdict:
                                resdict[word] = resdict[word] + 1
                            else:
                                resdict.update({word: 1})
                    restorant = soup2.find_all('div', {'class': "product-title show-mobile"})
                    listOnWords = restorant[0].string.replace("\n", "").split(" ")
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
    with open('Rank.csv', 'w') as csv_file:
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


FindRestorants('https://www.groo.co.il/category/188/food-drinks/tel-aviv/')


