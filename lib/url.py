import urllib.parse

def get(**kwargs):

    return ("?" + urllib.parse.urlencode(kwargs)) if kwargs else ''
