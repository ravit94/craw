import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import csv
import re

# Finding attractions with more then 3 stars:
def FindAtraction(url):
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
        for star in soup.findAll('div', {'class': "start_box"}):
            fullStar = star.__str__().count("very_big_star.png")
            halfStar = star.__str__().count("very_big_star_half.png")
            starts = float("{}.{}".format(fullStar,halfStar*5))
            if starts > 3 :
                soup2 = BeautifulSoup(plain_text, 'html.parser')
                atraction = soup2.find_all('span', {'class': "breadcrumb-item active"})
                listOnWords = atraction[0].string.replace("\n", "").split(" ")
                for word in listOnWords:
                    if word != '':
                        if word in resdict:
                            resdict[word] = resdict[word] + 1
                        else:
                            resdict.update({word: 1})
                # extract words from the description
                atraction = soup2.find_all('div', {'class': "text-content"})
                listOnWords = atraction[0].string.replace("\n", "").split(" ")
                for word in listOnWords:
                    if word != '' and not word.__contains__("\u200b"):
                        if word in resdict:
                            resdict[word] = resdict[word] + 1
                        else:
                            resdict.update({word: 1})
                atraction = soup2.find_all('div', {'class': "product-title show-mobile"})
                listOnWords = atraction[0].string.replace("\n", "").split(" ")
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
    with open('Stars.csv', 'w') as csv_file:
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


FindAtraction('https://www.groo.co.il/category/525/things-to-do-children/tel-aviv/')


