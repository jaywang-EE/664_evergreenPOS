import os
from django.utils import timezone
from datetime import date, datetime

TIME_SCHEMA = "%Y/%m/%d-%H:%M"

def ttos(tm):
    return tm.strftime(TIME_SCHEMA)

def stot(s):
    return datetime.strptime(s, TIME_SCHEMA)

