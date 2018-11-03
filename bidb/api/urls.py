from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^api/submit$', views.submit,
        name='submit'),
    url(r'^api/buildinfo/since/(?P<date>\d+)$', views.buildinfo_since,
        name='buildinfo_since'),
)
