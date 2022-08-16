import LOGDATA
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import seaborn as sns
resultsfileheaders = 'Macro, Micro, Description, Price, Type, Area Sqft, Bedrooms, When Listed, Listed by, Listing comment, Link, comment'
resultsfile = LOGDATA.DATA('C:\PythonProject\CompInt')
resultsfile.WRITE(resultsfileheaders)
total_skips = 0
total_pages = 9999
n = 1
choosepage=1
links = [["https://www.propertyfinder.ae/en/search?c=2&l=1863&ob=mr&page=1&rp=y&t=1","Rent"],
         ["","BUY"],
["","BUY"],
["","ResiRENT"]
]

for link in links:
    for n in range(total_pages):
        n += (choosepage-1)
        n += 1
        print(n)
        comment = link[1]
        print(comment)
        new_link = link[0].replace('page=1','page=%s'%(n))
        print(new_link)
        propertyfinder = new_link
        sns.set()
        headers = ({'User-Agent':
                    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        response = get(propertyfinder, headers=headers)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        house_containers = html_soup.find_all('div', class_="card-list__item")
        listings_on_page = len(house_containers)
        a = 0
        #print(house_containers[2])
        for a in range(listings_on_page):
            #print(a)
            first = house_containers[a]
            #Type
            type = html_soup.find_all('p', class_="card__property-amenity card__property-amenity--property-type")[a].text
            #Location
            location = first.find_all('span')[3].text
            location = location.replace(',','-')
            #Area
            try:
                area_str = html_soup.find_all('p', class_="card__property-amenity card__property-amenity--area")[a].text
            except:
                area_str = 'VOID'
            area_str = area_str.replace(',','')
            area_str = area_str.replace('sqft', '')
            #Bedrooms
            try:
                bedrooms = html_soup.find_all('p', class_="card__property-amenity card__property-amenity--bedrooms")[a].text
            except:
                bedrooms = 'VOID'

            #Title
            title = html_soup.find_all('h2', class_="card__title card__title-link")[a].text
            title = title.replace(',','-')
            if title.isalnum() != False:
                title = 'VOID'
            #Price
            price_str = first.find_all('span')[0].text

            def fix_price(price):
                price=price.replace('     ','')
                price=price.replace('\n','')
                price=price.replace('   ','')
                price=price.replace(',','')
                price=price.replace('AED/year','')
                return price
            price_str = fix_price(price_str)
            print(price_str)
            try:
                price_float = int(''.join(itertools.takewhile(str.isdigit, price_str )))
            except:
                price_float = '0'
            print(price_str)

            #url
            url = 'https://www.propertyfinder.ae/' + first.find_all('a')[0].get('href')
            response2 = get(url, headers=headers)
            html_soup2 = BeautifulSoup(response2.text, 'html.parser')
            #Description
            desc_container = html_soup2.find_all('div', class_="panel panel--style1 panel--style3")
            first = desc_container[0]
            description = first.find_all('h2')[0].text
            description = description.replace('        ','')
            description = description.replace(', ','-')
            description = description.replace('\n','')
            #print(description)
            #Listed
            listing_box = html_soup2.find_all('div', class_="property-page__legal-list-item property-page__legal-list-item--value")
            listed = listing_box[1].text
            #Lister
            listing_box = html_soup2.find_all('div', class_="text text--size2 property-agent__position")
            lister = listing_box[0].text
            #Micro
            location_box1 = html_soup2.find_all('div', class_="text text--size3 property-location__tower-name")
            micro = location_box1[0].text
            micro = micro.replace(', ', '-')
            print(micro)
            #Macro
            location_box2 = html_soup2.find_all('div', class_="text text--size3")
            macro = location_box2[0].text
            macro = macro.replace('Abu Dhabi, ', '')
            macro = macro.replace(',', '-')
            print(macro)

            #Macro

            #print(('\n' + str(location) + ',' + str(description) + ',' + str(title) + ',' + str(price_float) + ',' + str(type) +
                #              ',' + str(area_str) + ',' + str(bedrooms) +  ',' + str(listed) + ',' + str(lister) + ',' + str(url)))
            try:
                resultsfile.WRITE('\n' +str(macro) +',' + str(micro) + ',' + str(description) + ',' + str(price_float) + ',' + str(type) +
                                  ',' + str(area_str) + ',' + str(bedrooms) + ',' + str(listed) + ',' + str(lister)+ ',' + str(title) + ',' + str(url) + ',' + str(comment))
            except:
                print('Skipped Listing %s+1 on page %s'%(a,n))
                total_skips+=1
    print('number of skips:')
    print(total_skips)




