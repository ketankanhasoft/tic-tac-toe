
from django.conf.urls import url
from django.urls import include
from . import views

app_name = 'play'
urlpatterns=[
    url(r'^$',views.index, name="index"),
    url(r'^(?P<pk>\d+)/$', views.game, name='detail')
]