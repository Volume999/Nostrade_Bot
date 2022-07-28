from datetime import datetime
from bisect import bisect


def get_zodiac_sign_by_birth_date(birth_date: datetime):
    signs = [(1, 20, "Capricorn"), (2, 18, "Aquarius"), (3, 20, "Pisces"), (4, 20, "Aries"),
             (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 22, "Cancer"), (8, 23, "Leo"),
             (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
             (12, 31, "Capricorn")]
    return signs[bisect(signs, (birth_date.month, birth_date.day))][2]
