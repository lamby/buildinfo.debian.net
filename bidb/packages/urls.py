from django.conf.urls import url

from . import views


urlpatterns = (
    url(r'^source/(?P<name>[^/]+)$', views.source,
        name='source'),
    url(r'^binary/(?P<name>[^/]+)$', views.binary,
        name='binary'),
)
