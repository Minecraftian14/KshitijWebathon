from django.urls import path

from . import views

app_name = 'smartathon'

urlpatterns = [
    path('hw', views.hello_world, name='Hello World!'),
    path('create_user', views.create_user, name='create user dev ui'),
    path('create_user_service', views.create_user_service, name='create user service'),
    path('user_login', views.user_login, name='user login dev ui'),
    path('user_login_service', views.user_login_service, name='user login service'),
    path('user_logout_service', views.user_logout_service, name='user logout service'),
    path('create_competition_service', views.create_competition_service, name='user logout service'),
    path('list_competition_service', views.list_competition_service, name='user logout service'),
]