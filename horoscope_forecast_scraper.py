from datetime import datetime
import requests
from bs4 import BeautifulSoup


class HoroscopeScraper:
    pass


class AstroWorldScraper(HoroscopeScraper):
    def __init__(self, birth_datetime: datetime):
        self.birth_datetime = birth_datetime

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
        # print(soup.prettify())


scrp = AstroWorldScraper(datetime(2017, 2, 3, 8, 0, 0))
scrp.monthly_forecast(8, 2022)
