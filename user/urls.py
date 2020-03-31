from django.conf.urls import url

from user.views import IndexView, RegView


urlpatterns = [
    url('^reg$', RegView.as_view(), name='reg')
]
