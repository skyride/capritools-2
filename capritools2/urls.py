from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^dscan/$', views.dscan_home, name="dscan"),
    url(r'^dscan/submit/$', views.dscan_submit, name="dscan_submit")
]
