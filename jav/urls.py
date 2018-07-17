# Django package
from django.urls import path

# my application
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('login', views.user_login, name='user-login'),
        path('logout', views.user_logout, name='user-logout'),
        path('restricted', views.restricted, name='restricted-site'),
        path(''     , views.index, name='index'),
        path('about', views.about, name='about'),
        path('register',views.register, name='user-register'),
        path('actress/<slug:name>', views.view_actress, name='actress-detail'),
        path('add_actress', views.add_actress, name='add-actress'),
        path('actress/<slug:name>/add_movie', views.add_movie, name='add movie'),
        path('like_actress', views.like_actress, name="like-actress"),
        path('more', views.more_todo, name="more_todo"),
        path('add_todo', views.add_todo, name="add_todo"),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

