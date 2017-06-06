import random, string

from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings

from social_django.models import UserSocialAuth


def render_page(template, data, request):
    if "alert_type" in request.session:
        data['alert_type'] = request.session['alert_type']
        data['alert_message'] = request.session['alert_message']

        del request.session['alert_type']
        del request.session['alert_message']

    data['themes'] = settings.THEMES
    if "theme" in request.session:
        data['theme'] = request.session['theme']
    else:
        data['theme'] = settings.THEMES[0]

    try:
        data['social'] = request.user.social_auth.get(provider="eveonline")
    except Exception:
        data['social'] = None

    return render(request, template, data)


def random_key(length):
   return ''.join(random.choice(string.letters + string.digits) for i in range(length))
