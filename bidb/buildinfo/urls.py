from django.conf.urls import url, include

from . import views


urlpatterns = (
    url(r'', include('bidb.buildinfo.buildinfo_submissions.urls',
        namespace='submissions')),

    url(r'^(?P<sha1>\w{40})$', views.view,
        name='view'),
    url(r'^(?P<sha1>\w{40})/(?P<filename>.+)\.buildinfo$', views.raw_text,
        name='raw-text'),
    url(r'^(?P<sha1>\w{40})/(?P<filename>.+)$', views.view,
        name='view'),

    url(r'^api/v1/buildinfos/checksums/sha1/(?P<sha1>\w{40})$', views.checksums,
        name='checksums'),
)
