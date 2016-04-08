from django.conf.urls import url

from . import views

app_name = 'spacefinder'
urlpatterns = [

    # ༼ つ ◕_◕ ༽つ Regex pls

    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^space/(?P<slug>[\w-]+)/$', views.studyspace, name='studyspace'),
    url(r'^profile/(?P<slug>[\w-]+)/$', views.profile, name='profile'),
    url(r'^(?P<studyspace_id>[0-9]+)/vote/$', views.vote, name='vote'),

]
