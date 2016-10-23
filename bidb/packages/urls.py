from django.conf.urls import url

from . import views


urlpatterns = (
    url(r'^sources$', views.sources,
        name='sources'),

    url(r'^sources/(?P<name>[^/]+)$', views.source,
        name='source'),
    url(r'^binares/(?P<name>[^/]+)$', views.binary,
        name='binary'),
)
