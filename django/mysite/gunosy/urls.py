from django.conf.urls import url
from . import views


urlpatterns = [
     #url(r'^get/$', views.gunosy_get_url, name='gunosy_get_url'),
     #url(r'^/$', views.gunosy_helloworld, name='gunosy_helloworld'),
     url(r'^get/$', views.gunosy_naivebayes, name='gunosy_naivebayes'),#??

]
