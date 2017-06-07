from base64 import b64decode

from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^theme/(?P<theme>[a-zA-Z0-9]+)/(?P<ret>.+)/$', views.theme_submit, name="theme"),
    url(r'^logout/$', logout, {'next_page': "/"}, name="logout"),

    url(r'^account/scans/$', views.account_scans, name="account_scans"),

    url(r'^dscan/$', views.dscan_home, name="dscan"),
    url(r'^dscan/submit/$', views.dscan_submit, name="dscan_submit"),
    url(r'^dscan/(?P<key>[a-zA-Z0-9]+)/$', views.dscan_view, name="dscan_view"),

    url(r'^local/$', views.localscan_home, name="localscan"),
    url(r'^local/submit/$', views.localscan_submit, name="localscan_submit"),
    url(r'^local/(?P<key>[a-zA-Z0-9]+)/$', views.localscan_view, name="localscan_view"),

    url(r'^paste/$', views.paste_home, name="paste"),
    url(r'^paste/submit$', views.paste_submit, name="paste_submit"),
    url(r'^paste/(?P<key>[a-zA-Z0-9]+)/$', views.paste_view, name="paste_view"),

    url(r'^quickmath/$', views.quickmath_home, name="quickmath"),
    url(r'^quickmath/moongoo/$', views.quickmath_moongoo, name="moongoo"),
    url(r'^quickmath/implants/$', views.quickmath_implants, name="implants"),
]
