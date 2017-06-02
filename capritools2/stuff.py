import random, string

from django.shortcuts import render_to_response
from django.template import RequestContext


def render_page(template, data, request):
    return render_to_response(template, data, RequestContext(request))


def random_key(length):
   return ''.join(random.choice(string.letters + string.digits) for i in range(length))
