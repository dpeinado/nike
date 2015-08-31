 #-*- coding: utf-8 -*-
from datetime import datetime, date, timedelta

def alldaysinyear(year, day):
    """
    iterable con todos los day del year
    :param year:
    :param day:
    :return:
    """
    d = date(year, 1, 1)                    # January 1st
    d += timedelta(days = day - d.weekday())  # First Sunday
    while d.year == year:
        yield d
        d += timedelta(days = 7)