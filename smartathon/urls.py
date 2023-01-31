from django.urls import path

from . import views
from .view_utils import LOGGED_IN_USER_KEY

app_name = 'smartathon'
urlpatterns = [

    path('', views.list_competitions_command.dev_ui('competition_list', lambda req: {
        'c_list': views.list_competitions_command(req)['data'],
        LOGGED_IN_USER_KEY: req.session[LOGGED_IN_USER_KEY] if LOGGED_IN_USER_KEY in req.session else None
    }), name='list competitions dev ui'),
    path('list_competitions_service/', views.list_competitions_command.service(), name='list competitions service'),

    path('create_user_dev_ui/', views.create_user_command.dev_ui('signup'), name='create user dev ui'),
    path('create_user_service/', views.create_user_command.service(), name='create user service'),
    path('create_user_handler/', views.create_user_command.handler(), name='create user handler'),

    path('user_login_dev_ui/', views.user_login_command.dev_ui('login'), name='user login dev ui'),
    path('user_login_service/', views.user_login_command.service(), name='user login service'),
    path('user_login_handler/', views.user_login_command.handler(), name='user login handler'),

    path('user_logout_service/', views.user_logout_command.service(), name='user logout service'),
    path('user_logout_handler/', views.user_logout_command.handler(), name='user logout handler'),

    path('create_competition_dev_ui/', views.create_competition_command.dev_ui('new_competition'),
         name='create competition dev ui'),
    path('create_competition_service/', views.create_competition_command.service(), name='create competition service'),
    path('create_competition_handler/', views.create_competition_command.handler(), name='create competition handler'),

    path('create_team_dev_ui/<str:c_name>/<str:c_id>/', views.create_team_command.dev_ui('new_team'),
         name='create team dev ui'),
    # path('create_team_dev_ui/<str:c_name>/<str:c_id>', views.create_team_dev_ui, name='create team dev ui'),
    path('create_team_service/', views.create_team_command.service(), name='create team service'),
    path('create_team_handler/', views.create_team_command.handler(), name='create team handler'),

    path('create_join_request_dev_ui/<str:t_name>/<str:c_name>/',
         views.create_join_request_command.dev_ui('request_joining'), name='create join request dev ui'),
    path('create_join_request_service/', views.create_join_request_command.service(),
         name='create join request service'),
    path('create_join_request_handler/', views.create_join_request_command.handler(),
         name='create join request handler'),

    path('accept_join_request_service/', views.accept_join_request_command.service(),
         name='accept join request service'),
    path('accept_join_request_handler/', views.accept_join_request_command.handler(),
         name='accept join request handler'),

    path('list_team_details_dev_ui/', views.list_team_details_command.dev_ui('team_details', lambda req: {
        'data': views.list_team_details_command(req)['data'],
        LOGGED_IN_USER_KEY: req.session[LOGGED_IN_USER_KEY] if LOGGED_IN_USER_KEY in req.session else None
    }), name='list team details dev ui'),
    path('list_team_details_service/', views.list_team_details_command.service(), name='list team details service'),
]
