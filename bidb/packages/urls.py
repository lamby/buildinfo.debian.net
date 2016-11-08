from django.conf.urls import url

from . import views


urlpatterns = (
    url(r'^sources$', views.sources,
        name='sources'),
    url(r'^binaries$', views.binaries,
        name='binaries'),

    url(r'^sources/(?P<name>[^/]+)$', views.source,
        name='source'),
    url(r'^sources/(?P<name>[^/]+)/(?P<version>[^/]+)$', views.source_version,
        name='source-version'),
    url(r'^binaries/(?P<name>[^/]+)$', views.binary,
        name='binary'),
)
