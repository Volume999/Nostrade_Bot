from datetime import datetime
import requests


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
        print(req.text)


scrp = AstroWorldScraper(datetime(2022, 2, 2, 8, 0, 0))
scrp.monthly_forecast(8, 2022)
