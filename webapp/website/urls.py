from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^website/$', views.index),
    url(r'^$', views.homepage),
]
