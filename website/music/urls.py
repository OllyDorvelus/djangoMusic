from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'music'


urlpatterns = [
    # /music/
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /music/71/
   # url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # /music/album/add
    url(r'^album/add/$', views.AlbumCreate.as_view(), name='album-add'),
    #url(r'^me/$', views.test, name='test'),

    #/music/<album_id>/favorite/
    #url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    # /music/album/2/
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
    #/music/album/2/delete
    url(r'^(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),

    url(r'^add_song/$', views.SongCreate.as_view(), name="add_song"),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    url(r'^login/$', views.UserLoginFormView.as_view(), name="login"),

    url(r'^logout/$', views.logout_view, name="logout"),
]
