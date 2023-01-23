from django.urls import path

from . import views

app_name = 'smartathon'
urlpatterns = [
    path('hw', views.hello_world, name='Hello World!'),

    path('create_user_dev_ui', views.create_user_dev_ui, name='create user dev ui'),
    path('create_user_service', views.create_user_service, name='create user service'),
    path('create_user_handler', views.create_user_handler, name='create user handler'),

    path('user_login_dev_ui', views.user_login_dev_ui, name='user login dev ui'),
    path('user_login_service', views.user_login_service, name='user login service'),
    path('user_login_handler', views.user_login_handler, name='user login handler'),

    path('user_logout_service', views.user_logout_service, name='user logout service'),
    path('user_logout_handler', views.user_logout_handler, name='user logout handler'),

    path('create_competition_dev_ui', views.create_competition_dev_ui, name='create competition dev ui'),
    path('create_competition_service', views.create_competition_service, name='create competition service'),
    path('create_competition_handler', views.create_competition_handler, name='create competition handler'),

    path('create_team_dev_ui/<str:compe>', views.create_team_dev_ui, name='create team dev ui'),
    path('create_team_service', views.create_team_service, name='create team service'),
    path('create_team_handler', views.create_team_handler, name='create team handler'),

    path('create_join_request_dev_ui/<str:tname>/<str:cname>', views.create_join_request_dev_ui,
         name='create join request dev ui'),
    path('create_join_request_service', views.create_join_request_service, name='create join request service'),
    path('create_join_request_handler', views.create_join_request_handler, name='create join request handler'),

    path('', views.list_competitions_handler, name='list competitions handler'),
    path('list_competitions_service', views.list_competitions_service, name='list competitions service'),
]
