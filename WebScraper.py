from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
startUrl ="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome('Driver/chromedriver')
browser.get(startUrl)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity"]
planetdata = []
newplanetdata = []
def scrape():
    for i in range (0,428):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            currentpagenum = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            if currentpagenum<i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentpagenum>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ultag in soup.find_all("ul",attrs = {"class","exoplanet"}):
            litags = ultag.find_all("li")
            templist = []
            for index,litag in enumerate(litags):
                if index == 0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
            hyperlink_litags = litags[0]
            templist.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planetdata.append(templist)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} pagedone")

def scrapemoredata(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        templist = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0]) 
                except:
                    templist.append("")
        newplanetdata.append(templist)
    except:
        time.sleep(1)
        scrapemoredata(hyperlink)

scrape()
for index,data in enumerate(planetdata):
    scrapemoredata(data[5])
    print(f"{i} pagedone 2")
finalplanetdata = []
for index,data in enumerate(planetdata):
    newplanetelement = newplanetdata(index)
    newplanetelement = [elem.replace("\n","")for elem in newplanetelement]
    newplanetelement = newplanetelement[:7]
    finalplanetdata.append(data+newplanetelement)
with open("MyScrapedData.csv","w")as f:
    csvwriter = csv.writer(f)
    csv.writer.writerow(headers)
    csv.writer.writerows(finalplanetdata)
