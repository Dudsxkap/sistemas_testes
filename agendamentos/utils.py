import re

import pytz
from django.conf import settings
from django.utils import timezone


def strftime_local(data_hora, formatador):
    try:
        data_local = timezone.localtime(data_hora, pytz.timezone(settings.TIME_ZONE))
        return data_local.strftime(formatador)
    except Exception as e:
        return data_hora.strftime(formatador)


def digits(txt):
    if txt:
        return re.sub(r'\D', '', txt)
    return txt
