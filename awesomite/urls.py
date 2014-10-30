from django.conf.urls import patterns, url
from awesomite import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        # url(r'^add/$', views.addtodo, name='addtodo'),
        )
