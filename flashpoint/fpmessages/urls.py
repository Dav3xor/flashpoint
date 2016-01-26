from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^stat/get', views.stats, name='stats')
]
