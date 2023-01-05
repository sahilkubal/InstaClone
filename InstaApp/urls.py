from xml.dom.minidom import Document
from django.urls import path 
from . import views as v
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', v.index, name = "index"),
    path('signup', v.signup, name='signup'),
    path('signin', v.signin, name='signin'),
    path('search', v.search, name='search'),
    path('explore', v.explore, name='explore'),
    path('profile/<str:pk>', v.profile, name='profile'),
    path('follow', v.follow, name='follow'),
    path('upload_post', v.upload_post, name='upload_post'),
    path('like-post', v.like_post, name='like-post'),
    path('settings', v.Settings, name='settings'),
    path('pwdreset', v.Password_reset, name='pwdreset'),
    path('logout', v.UserLogout, name='logout'),
]

