import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

import database

url = "https://www.holiday.by/tours/lastminute"
FILE_NAME = 'test.csv'

def parser(url = url):
    resualt_list = {'href': [],
                    'title': [],
                    'costbel': [],
                    'costdoll': [],
                    'countrygo': [],
                    'whenfly': [],
                    'daystrip': [],
                    }

    r = requests.get(url)
    soup = BS(r.text, 'html.parser')

    """название общаги"""
    title = soup.find_all('div', class_='h4 tour-thumbnail__name')
    for hotel in title:
        resualt_list['href'].append('https://www.holiday.by' + hotel.a['href'])
    """ссылка"""
    href = soup.find_all('p', class_='overflow')
    for tour in title:
        resualt_list['title'].append(tour.a['title'])


    """стоймость в белках"""
    costbel = soup.find_all('div', class_="tour-thumbnail__price-value")
    for cost in costbel:
        resualt_list['costbel'].append(cost.text.replace(' BYN', ''))

    """стоймость в баксах"""
    costdoll = soup.find_all('div', class_="tour-thumbnail__price-currency")
    for cost2 in costdoll:
        resualt_list['costdoll'].append(int(cost2.text.strip().replace('$', '').replace('€', '').replace(' ', '')))

     # """в какую страну"""
    countrygo = soup.find_all('ul', class_="tour-thumbnail__tags")
    for country in countrygo:
        resualt_list['countrygo'].append(country.text[1:7].replace(' ', '').replace('\n', '').replace('Д', ''))


    """когда вылет и н сколько дней"""
    whenfly = soup.find_all('div', class_="tour-thumbnail__tour-time tour-thumbnail__tour-time_full")
    for days in whenfly:
        resualt_list['daystrip'].append(int(days.text[:2].replace(' ', '')))

    """сколько дней"""
    daystrip = soup.find_all('div', class_="tour-thumbnail__tour-time tour-thumbnail__tour-time_full")
    for days in daystrip:
        resualt_list['whenfly'].append(days.text)




    return resualt_list

df = pd.DataFrame(data=parser())
df.to_csv(FILE_NAME)

def get_text(url):
#из URL вытаскиваем html
    r = requests.get(url)
    text = r.text
    return text

f = open('test.csv', 'r', encoding='UTF-8')
test = f.read()
f.close()
