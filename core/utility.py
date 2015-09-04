 #-*- coding: utf-8 -*-
from datetime import datetime, date, timedelta

def get_range_dates_list(inicio, fin):
    base = inicio
    cuantos = (fin - inicio).days
    date_list = [base + timedelta(days=x) for x in range(0, cuantos+1)]
    return date_list

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