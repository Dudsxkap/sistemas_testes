import re


def digits(txt):
    if txt:
        return re.sub(r'\D', '', txt)
    return txt
