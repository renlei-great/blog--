from django.conf.urls import url

from .views import pub, getall, get


urlpatterns = [
    url('^pub$', pub, name='pub'),
    url('^(?P<post_id>\d+)$', get, name='get'),
    url('^$', getall, name='getall'),
]
