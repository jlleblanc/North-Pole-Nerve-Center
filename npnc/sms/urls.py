from django.conf.urls.defaults import patterns, include, url
from views import recv_sms


urlpatterns = patterns('',
    url(r'^reply/', recv_sms),
)

