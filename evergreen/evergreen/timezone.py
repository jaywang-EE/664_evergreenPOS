import os
from django.utils import timezone
from datetime import datetime
from .settings import TIME_ZONE
import pytz

#TIME_ZONE = settings.TIME_ZONE
TIME_SCHEMA = "%Y/%m/%d-%H:%M"
tz = pytz.timezone(TIME_ZONE)

def stot(s):
    if not s: return s
    return tz.localize(datetime.strptime(s, TIME_SCHEMA), is_dst=None)

def get_now():
    return timezone.now()
