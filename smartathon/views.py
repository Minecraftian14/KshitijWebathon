from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import *
from django.shortcuts import render


def hello_world(req):
    return HttpResponse("Hello world, the server is online!")


def create_user_command(req: HttpRequest):
    try:
        uname = req.POST['uname']

        if len(uname) == 0:
            return {'status': 'fail', 'reason': 'invalid user name'}

        if len(User.objects.filter(uname=uname)) > 0:
            return {'status': 'fail', 'reason': 'user already exists'}

        upass = req.POST['upass']

        if len(upass) < 8:
            return {'status': 'fail', 'reason': 'invalid password'}

        umail = req.POST['umail']

        if len(uname) == 0:
            return {'status': 'fail', 'reason': 'invalid user name'}

        obj = User(uname=uname, upass=upass, umail=umail)
        obj.save()

        return {'status': 'success', 'reason': 'Account successfully create.'}

    except Exception as e:
        print(repr(e))
        return {'status': 'fail', 'reason': 'absolute failure'}


def create_user_dev_ui(req: HttpRequest):
    return render(req, 'devui/signup.html', {})


def create_user_service(req: HttpRequest):
    res = create_user_command(req)
    return JsonResponse(res)


def create_user_handler(req: HttpRequest):
    return render(req, 'devui/success.html', create_user_command(req))


def user_login_command(req: HttpRequest):
    try:
        uname = req.POST['uname']

        try:
            obj = User.objects.get(uname=uname)
        except Exception as e:
            print(repr(e))
            return {'status': 'fail', 'reason': 'user does not exists'}

        upass = req.POST['upass']

        if obj.password != upass:
            return {'status': 'fail', 'reason': 'invalid password'}

        req.session['uname'] = obj.name

        return {'status': 'success', 'reason': 'login successful'}

    except Exception as e:
        print(repr(e))
        return {'status': 'fail', 'reason': 'absolute failure'}


def user_login_dev_ui(req: HttpRequest):
    return render(req, 'devui/login.html', {})


def user_login_service(req: HttpRequest):
    return JsonResponse(user_login_command(req))


def user_login_handler(req: HttpRequest):
    return render(req, 'devui/success.html', user_login_command(req))


def user_logout_command(req: HttpRequest):
    try:
        del req.session['uname']
        return {'status': 'success', 'reason': 'logout successful'}

    except Exception as e:
        print(repr(e))
        return {'status': 'fail', 'reason': 'absolute failure'}


def user_logout_service(req: HttpRequest):
    return JsonResponse(user_logout_command(req))


def user_logout_handler(req: HttpRequest):
    return render(req, 'devui/success.html', user_logout_command(req))


def create_competition_command(reg: HttpRequest):
    try:
        cname = reg.POST['cname']
        cdesc = reg.POST['cdesc']
        cdate = reg.POST['cdate']
        cvenue = reg.POST['cvenue']
        max_members = reg.POST['max_members']

        Competition(cname=cname, cdesc=cdesc, cdate=cdate, cvenue=cvenue, max_members=max_members).save()

        return {'status': 'success', 'reason': 'competition successfully created'}

    except Exception as e:
        print(repr(e))
        return {'status': 'fail', 'reason': 'absolute failure'}


def create_competition_dev_ui(req: HttpRequest):
    return render(req, 'devui/new_competition.html', {})


def create_competition_service(req: HttpRequest):
    return JsonResponse(create_competition_command(req))


def create_competition_handler(req: HttpRequest):
    return render(req, 'devui/success.html', create_competition_command(req))


def create_team_command(reg: HttpRequest):
    try:
        tname = reg.POST['tname']
        compe = Competition.objects.get(cname=reg.POST['compe'])
        vacant_members = compe.max_members - 1
        tfref = 0

        TeamDetails(tname=tname, compe=compe.name, vacant_members=vacant_members, tfref=tfref).save()

        return {'status': 'success', 'reason': 'team successfully created'}

    except Exception as e:
        print(repr(e))
        return {'status': 'fail', 'reason': 'absolute failure'}


def create_team_dev_ui(req: HttpRequest, compe):
    return render(req, 'devui/new_team.html', {'compe': compe})


def create_team_service(req: HttpRequest):
    return JsonResponse(create_team_command(req))


def create_team_handler(req: HttpRequest):
    return render(req, 'devui/success.html', create_team_command(req))


def list_competitions_command(reg: HttpRequest):
    try:
        c_list = []
        for c in Competition.objects.all():
            c_list.append({
                'cname': c.name, 'cdesc': c.description, 'cdate': c.date, 'cvenue': c.venue, 'max_members': c.max_members,
                'teams': [t.table() for t in TeamDetails.objects.filter(compe=c.name)]
            })
        return {'status': 'success', 'reason': 'query successful', 'data': c_list}

    except Exception as e:
        print(repr(e))
        return {'status': 'fail', 'reason': 'absolute failure'}


def list_competitions_service(req: HttpRequest):
    return JsonResponse(list_competitions_command(req))


def list_competitions_handler(req: HttpRequest):
    return render(req, 'devui/competition_list.html',
                  {'c_list': list_competitions_command(req)['data'], 'session': 'uname' in req.session})


def create_join_request_command(req: HttpRequest):
    try:
        cname = req.POST['cname']
        tname = req.POST['tname']
        rmsge = req.POST['rmsge']

        Request(cname=cname, tname=tname, rmsge=rmsge).save()

        return {'status': 'succes', 'reason': 'request sent'}

    except Exception as e:
        print(repr(e))
        return {'status': 'fail', 'reason': 'absolute failure'}


def create_join_request_dev_ui(req: HttpRequest, tname, cname):
    return render(req, 'devui/request_joining.html', {'tname': tname, 'cname': cname})


def create_join_request_service(req: HttpRequest):
    return JsonResponse(create_join_request_command(req))


def create_join_request_handler(req: HttpRequest):
    return render(req, 'devui/success.html', create_join_request_command(req))
