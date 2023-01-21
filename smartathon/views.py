from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import *
from django.shortcuts import render


def hello_world(req):
    return HttpResponse("Hello world, the server is online!")


def create_user(req: HttpRequest):
    return render(req, 'devui/signup.html', {})


def user_login(req: HttpRequest):
    return render(req, 'devui/login.html', {})


def create_user_service(req: HttpRequest):
    try:
        uname = req.POST['uname']

        if len(uname) == 0:
            return JsonResponse({'status': 'fail', 'reason': 'invalid user name'})

        if len(User.objects.filter(uname=uname)) > 0:
            return JsonResponse({'status': 'fail', 'reason': 'user already exists'})

        upass = req.POST['upass']

        if len(upass) < 8:
            return JsonResponse({'status': 'fail', 'reason': 'invalid password'})

        umail = req.POST['umail']

        if len(uname) == 0:
            return JsonResponse({'status': 'fail', 'reason': 'invalid user name'})

        obj = User(uname=uname, upass=upass, umail=umail)
        obj.save()

        return JsonResponse({'status': 'success'})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'fail', 'reason': 'absolute failure'})


def user_login_service(req: HttpRequest):
    try:
        uname = req.POST['uname']

        try:
            obj = User.objects.get(uname=uname)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'fail', 'reason': 'user does not exists'})

        upass = req.POST['upass']

        if obj.upass != upass:
            return JsonResponse({'status': 'fail', 'reason': 'invalid password'})

        req.session['uname'] = obj.id

        return JsonResponse({'status': 'success'})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'fail', 'reason': 'absolute failure'})


def user_logout_service(req: HttpRequest):
    try:
        del req.session['uname']
        return JsonResponse({'status': 'success'})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'fail', 'reason': 'absolute failure'})


def create_competition_service(reg: HttpRequest):
    try:
        cname = reg.POST['cname']
        cdesc = reg.POST['cdesc']

        Competition(cname=cname, cdesc=cdesc).save()

        return JsonResponse({'status': 'success'})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'fail', 'reason': 'absolute failure'})


def list_competition_service(reg: HttpRequest):
    try:
        c_list = []
        for c in Competition.objects.all():
            c_list.append({
                'cname': c.cname, 'cdesc': c.cdesc,
                'teams': [t.table() for t in TeamDetails.objects.filter(cid=c.cid)]
            })
        return JsonResponse({'status': 'success', 'data': c_list})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'fail', 'reason': 'absolute failure'})
