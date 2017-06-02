import random, string

from django.shortcuts import render
from django.template import RequestContext


def render_page(template, data, request):
    return render(request, template, data)


def random_key(length):
   return ''.join(random.choice(string.letters + string.digits) for i in range(length))
