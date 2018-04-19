from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^createuser$', views.create_user),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^post_quote$', views.post_quote),
    url(r'^users/(?P<id>\d+)$', views.displayuserquotes),
    url(r'^addquote/(?P<id>\d+)$', views.addquote),
    url(r'^removequote/(?P<id>\d+)$', views.removequote),
]