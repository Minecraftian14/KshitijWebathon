from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import *
from .view_utils import *
from django.shortcuts import render
import re


@backend_command
def create_user_command(req: HttpRequest):
    name = from_post(req, 'name')
    verify_name(name)
    assert_expr(User.objects.filter(pk=name).count() == 0, 'username is already in use')

    password = from_post(req, 'password')
    assert_expr(len(password) >= 8
                and count(r'[0-9]', password) > 0
                and count(r'[A-Z]', password) > 0
                and count(r'[a-z]', password) > 0
                and count(r'[@$!%*#?&]', password) > 0,
                '''
                invalid password, the password must contain at least one digit, at least one capital case
                character, at least one lower case character and at least one special symbol (@$!%*#?&)
                ''')

    mail = from_post(req, 'mail')
    assert_expr(re.match(r'^([a-zA-Z0-9+_.-]+)@([a-zA-Z0-9-]+)(\.[a-zA-Z]{2,5}){1,2}$', mail),
                'invalid mail format')

    User(name=name, password=password, mail=mail).save()

    return success('account successfully created')


@backend_command
def user_login_command(req: HttpRequest):
    name = from_post(req, 'name')
    verify_name(name)

    user = do_or_die(lambda: User.objects.get(name=name), 'account does not exists')

    password = from_post(req, 'password')
    assert_expr(user.password == password, 'invalid password')

    req.session['logged_in_user'] = name

    return success('login successful')


@backend_command
def user_logout_command(req: HttpRequest):
    del req.session['logged_in_user']
    return success('logout successful')


@backend_command
def create_competition_command(req: HttpRequest):
    name = from_post(req, 'name')
    verify_name(name)

    max_members = from_post(req, 'max_members')
    assert_expr(int(max_members) >= 2, 'there should be at least 2 members in a team.')

    description = from_post(req, 'description')
    date = from_post(req, 'date')
    venue = from_post(req, 'venue')

    Competition(name=name, description=description, date=date, venue=venue, max_members=max_members).save()

    return success('competition successfully created')


@backend_command
def create_team_command(req: HttpRequest):
    name = from_post(req, 'name')
    verify_name(name)

    c_id = from_post(req, 'c_id')
    competition = do_or_die(lambda: Competition.objects.get(pk=c_id), malnourished_form('competition name'))

    u_name = req.session['logged_in_user']
    do_or_die(lambda: User.objects.get(pk=u_name), malnourished_form('affiliated username'))

    assert_expr(TeamDetails.objects.filter(competition_id=c_id, members={'u_name': u_name}).count() == 0,
                'you can not join two teams in the same competition')

    competition.teamdetails_set.create(name=name,
                                       vacant_spaces=competition.max_members - 1,
                                       members=[{'u_name': u_name}])

    return success('team successfully created')


@backend_command
def create_join_request_command(req: HttpRequest):
    t_name = from_post(req, 't_name')
    u_name = req.session['logged_in_user']
    assert_expr(Request.objects.filter(author__name=u_name, team__name=t_name).count() == 0,
                "you can't send request to the same team again")
    assert_expr(TeamDetails.objects.filter(name=t_name, members={'u_name': u_name}).count() == 0,
                "you are already a member")

    request_message = from_post(req, 'request_message')

    user = do_or_die(lambda: User.objects.get(pk=u_name), "the username does not exist")
    team = do_or_die(lambda: TeamDetails.objects.get(name=t_name), "the requested team does not exist")
    assert_expr(team.vacant_spaces > 0, "the team just accepted someone else...")

    Request(author=user, team=team, request_message=request_message).save()
    team.vacant_spaces -= 1
    team.save()

    return success('request sent')


@backend_command
def accept_join_request_command(req: HttpRequest):
    r_id = from_post(req, 'r_id')
    request = do_or_die(lambda: Request.objects.get(pk=r_id), 'invalid request identity')
    u_name = request.author.name

    request.team.members = request.team.members + [{'u_name': u_name}]
    assert_expr(request.team.vacant_spaces > 0, 'illegal state! team must have at least one vacant space')
    request.team.vacant_spaces = request.team.vacant_spaces - 1
    request.team.save()
    request.delete()

    return success('request accepted')


@backend_command
def list_competitions_command(req: HttpRequest):
    c_list = []
    for c in Competition.objects.all():
        teams = c.teamdetails_set.filter(vacant_spaces__gt=0)
        if 'logged_in_user' in req.session:
            teams = teams.exclude(members={'u_name': req.session['logged_in_user']})
        c_list.append({
            'id': c.pk, 'name': c.name, 'description': c.description, 'date': c.date,
            'venue': c.venue, 'max_members': c.max_members,
            'teams': [t.short_table() for t in teams]
        })
    return success('query successful', c_list)


@backend_command
def list_team_details_command(req: HttpRequest):
    u_name = req.session['logged_in_user']
    user = do_or_die(lambda: User.objects.get(pk=u_name), "the username does not exist")
    teams = TeamDetails.objects.filter(members={'u_name': u_name})

    your_teams = [t.long_table() for t in teams]
    requests = [r.team.long_table() for r in user.request_set.all()]
    pending_requests = []

    for t in teams.filter(vacant_spaces__gt=0):
        pending_requests.append({
            'team': t.long_table(),
            'requests': [r.table() for r in t.request_set.all()]
        })

    return success('query successful', {
        'your_teams': your_teams,
        'requests': requests,
        'pending_requests': pending_requests,
    })


def list_team_details_handler(req: HttpRequest):
    return render(req, 'devui/team_details.html', {

    })
