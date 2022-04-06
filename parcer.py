import requests
from bs4 import BeautifulSoup as BS
import pandas as pd


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
    hot_tour_hotel = soup.find_all('div', class_='h4 tour-thumbnail__name')
    for hotel in hot_tour_hotel:
        resualt_list['href'].append('https://www.holiday.by' + hotel.a['href'])
    """ссылка"""
    information = soup.find_all('p', class_='overflow')
    for tour in hot_tour_hotel:
        resualt_list['title'].append(tour.a['title'])


    """стоймость в белках"""
    hot_tour_hotel_cost = soup.find_all('div', class_="tour-thumbnail__price-value")
    for cost in hot_tour_hotel_cost:
        resualt_list['costbel'].append(cost.text.replace(' BYN', ''))

    """стоймость в баксах"""
    hot_tour_hotel_cost2 = soup.find_all('div', class_="tour-thumbnail__price-currency")
    for cost2 in hot_tour_hotel_cost2:
        resualt_list['costdoll'].append(cost2.text.strip().replace('$', '').replace('€', ''))

     # """в какую страну"""
    country_go = soup.find_all('ul', class_="tour-thumbnail__tags")
    for country in country_go:
        resualt_list['countrygo'].append(country.text)

    """когда вылет и н сколько дней"""
    how_days = soup.find_all('div', class_="tour-thumbnail__tour-time tour-thumbnail__tour-time_full")
    for days in how_days:
        resualt_list['daystrip'].append(days.text[:2])

    """когда вылет и н сколько дней"""
    where_and_how_days = soup.find_all('div', class_="tour-thumbnail__tour-time tour-thumbnail__tour-time_full")
    for days in where_and_how_days:
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
