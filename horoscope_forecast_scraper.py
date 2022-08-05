from datetime import datetime
import requests
from bs4 import BeautifulSoup
from settings import *
from Library import *


class HoroscopeScraper:
    pass


class AstroWorldScraper(HoroscopeScraper):
    def __init__(self, birth_datetime: datetime):
        self.birth_datetime = birth_datetime
        self.zodiac_sign = None if birth_datetime is None else get_zodiac_sign_by_birth_date(birth_datetime)

    def monthly_forecast(self, prediction_month, prediction_year):
        url = r'https://www.astroworld.ru/horon/mes_res.htm'
        payload = {
            "den": self.birth_datetime.day,
            "mes": self.birth_datetime.month,
            "god": self.birth_datetime.year,
            "chas": self.birth_datetime.hour,
            "minuta": self.birth_datetime.minute,
            "mesp": prediction_month,
            "godp": prediction_year,
            "cityCode": 12278
        }
        req = requests.post(url=url, data=payload)
        soup = BeautifulSoup(req.text, features='html.parser')
        soup = soup.find("div", {"class": "osn"})
        # print(soup)
        soup = filter(lambda item: len(list(item.attrs)) == 0, soup.find_all('p'))
        # print(list(soup)[1])
        # print(list(soup))
        res = []
        for forecast in soup:
            # print(forecast)
            title = forecast.find('strong')
            text = forecast.text
            message = ""

            if title is not None:
                message += f"{title.text}"

            if text is not None:
                message += f"\n{text.replace(title.text, '') if title is not None else text}\n"

            if message.strip() != '':
                res.append(message)

        return res

    def yearly_forecast(self, sign):
        index = get_zodiac_index_by_sign(sign)
        year = datetime.now().year
        url = f'https://www.astroworld.ru/horoscope{year}_{"{:02}".format(index + 1)}.htm'
        print(url)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, features='html.parser')
        # print(soup.prettify())
        # soup = soup.find("div", {"class": "osn"})
        soup = filter(lambda item: len(list(item.attrs)) == 0, soup.find_all('p'))
        soup = filter(lambda item: len(item.find_all('a')) == 0, soup)
        # print(list(soup)[1])
        # print(list(soup))
        res = []
        for forecast in soup:
            # print(forecast.prettify())
            # print(len(forecast.find_all('a')))
            # print(forecast)
            title = forecast.find('strong')
            text = forecast.text
            message = ""

            if title is not None:
                message += f"{title.text}"

            if text is not None:
                message += f"\n{text.replace(title.text, '') if title is not None else text}\n"

            if message.strip() != '':
                res.append(message)

        return res

    def today_forecast(self, sign):
        sign_translated = ZODIAC_SIGNS_TRANSLATED[sign]
        url = f'https://www.astroworld.ru/segodnja-{sign_translated}.htm'
        print(url)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, features='html.parser')
        # print(soup.prettify())
        # soup = soup.find("div", {"class": "osn"})
        soup = filter(lambda item: len(list(item.attrs)) == 0, soup.find_all('p'))
        soup = filter(lambda item: len(item.find_all('a')) == 0, soup)
        # print(list(soup)[1])
        # print(list(soup))
        res = []
        for forecast in soup:
            # print(forecast.prettify())
            # print(len(forecast.find_all('a')))
            # print(forecast)
            title = forecast.find('strong')
            text = forecast.text
            message = ""

            if title is not None:
                message += f"{title.text}"

            if text is not None:
                message += f"\n{text.replace(title.text, '') if title is not None else text}\n"

            if message.strip() != '':
                res.append(message)

        return res

scrp = AstroWorldScraper(datetime(2017, 2, 3, 8, 0, 0))
# scrp.monthly_forecast(8, 2022)
# scrp.yearly_forecast('Virgo')
# print(scrp.today_forecast('Virgo'))
