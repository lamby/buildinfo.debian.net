from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^api/submit$', views.submit,
        name='submit'),
)
