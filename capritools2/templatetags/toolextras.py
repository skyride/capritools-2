from django import template
from django.conf import settings
from base64 import b64encode


register = template.Library()

def highlight(value):
    if value in settings.DSCAN_HIGHLIGHTS:
        return settings.DSCAN_HIGHLIGHTS[value]
    else:
        return "active"


def b64(value):
    return b64encode(value)


register.filter('highlight', highlight)
register.filter('b64', b64)
