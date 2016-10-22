from django.conf import settings
from django.conf.urls import include, url
from django.views.static import serve


urlpatterns = (
    url(r'', include('bidb.api.urls',
        namespace='api')),
    url(r'', include('bidb.buildinfo.urls',
        namespace='buildinfo')),
    url(r'', include('bidb.packages.urls',
        namespace='packages')),
    url(r'', include('bidb.static.urls',
        namespace='static')),
)

if settings.DEBUG:
    urlpatterns += (
        url(r'^storage/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
