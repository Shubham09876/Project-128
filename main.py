import time
import csv
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_brown_dwarfs'
browser = webdriver.Chrome('chromedriver.exe')
browser.get(url)
time.sleep(10)

headers = ['star' , 'constellation' , 'right ascension' , 'Declination' , 'app. mag.' , 'distance' , 'spectral_type' , 'brown dwarf' , 'mass' , 'radius' , 'orbital period' , 'smimajor axis', 'eccentricity' , 'discovery year' , 'luminosity' , 'surface gravity' , 'temperature' , 'metallicity' , 'rotation' , 'age']
starData = []
newStarData = []

def scrape():

    for i in range(1 , 201):
        while True: 
            time.sleep(2)
        
        soup = BeautifulSoup(browser.page_source , 'html.parser')

        currentPageNumber = int(soup.find_all('input' , attrs = {'class' , 'page_num'})[0].get('value'))

        if currentPageNumber > i:
            browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            
        elif currentPageNumber < i:
            browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()

        else:
            break

    for ulTag in soup.find_all('ul' , attrs = {'class' , 'dwarf star'}):
        liTag = ulTag.find_all('li')
        tempList = []
    
        for index , li in enumerate(liTag):
            if index == 0:
                tempList.append(li.find_all('a')[0].contents[0])
            else:
                try:
                    tempList.appned(li.contents[0])
                except:
                    tempList.append("")
    
        hyperlinkLiTag = liTag[0]
        tempList.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs" + hyperlinkLiTag.find_all('a' , href = True)[0]['href'])

        starData.append(tempList)

    browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

def scrapeMoreData(hyperlink):

    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content , 'html.parser')
        tempList = []

        for tr in soup.find_all('tr' , attrs = {'class' , 'details'}):
            td = tr.find_all('td')

            for tdTag in td:
                try:
                    tempList.append(tdTag.find_all('div' , attrs = {'class' , 'value'})[0].contents[0])
                except:
                    tempList.append('')
            
        newStarData.append(tempList)

    except:
        time.sleep(1)
        scrapeMoreData(hyperlink)
    
scrape()

for index , i in enumerate(planetData):
    scrapeMoreData(i[5])

finalStarData = []

for index , j in enumerate(planetData):
    newData = newPlanetData[index]
    newData = [new.replace('\n' , '') for new in newData ]
    newData = newData[:7]

    finalStarData.append(j + newData)

with open('final.csv' , 'w') as f:
    csvWriter = csv.writer(f)
    csvWriter.writeRow(headers)
    csvWriter.writeRows(finalStarData)


