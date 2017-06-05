import random, string

from django.shortcuts import render
from django.template import RequestContext


def render_page(template, data, request):
    if "alert_type" in request.session:
        data['alert_type'] = request.session['alert_type']
        data['alert_message'] = request.session['alert_message']

        del request.session['alert_type']
        del request.session['alert_message']

    return render(request, template, data)


def random_key(length):
   return ''.join(random.choice(string.letters + string.digits) for i in range(length))
