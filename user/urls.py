from django.conf.urls import url

from user.views import IndexView, RegView, LoginView, test


urlpatterns = [
    url('^reg$', RegView.as_view(), name='reg'),
    url('^login$', LoginView.as_view(), name='login'),
    url('^test$', test),
]
