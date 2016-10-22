from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^(?P<sha1>\w{40})/(?P<filename>[^/]+)/(?P<slug>\w+).buildinfo$', views.view,
        name='view'),
)
