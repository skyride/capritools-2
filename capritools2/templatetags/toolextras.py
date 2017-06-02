from django import template
from django.conf import settings


register = template.Library()

def highlight(value):
    if value in settings.DSCAN_HIGHLIGHTS:
        return settings.DSCAN_HIGHLIGHTS[value]
    else:
        return "active"

register.filter('highlight', highlight)
