import traceback

import re
from typing import Callable

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from smartathon.models import User


def fail(reason, data='null'):
    return {'status': 'fail', 'reason': reason, 'data': data}


def success(reason, data='null'):
    return {'status': 'success', 'reason': reason, 'data': data}


LOGGED_IN_USER_KEY = 'logged_in_user'
DEFAULT_FAIL_MESSAGE = fail('server side exception based failure')


def count(pattern, string):
    return len(re.findall(pattern, string))


class ProperException(Exception):
    def __init__(self, response, exception=None, *args):
        super().__init__(*args)
        self.response = response
        self.exception = exception


def verify_name(value):
    if len(value) <= 5:
        raise ProperException('names smaller than or equal to 5 characters are reserved')

    if not value.replace(' ', '').isalnum():
        raise ProperException('only alphanumeric characters and spaces are allowed as names')


def do_or_die(action, emsg):
    try:
        return action()
    except Exception as e:
        raise ProperException(emsg, e)


def malnourished_form(key):
    return f'server did not receive any key named {key}'


def from_post(req, key):
    return do_or_die(lambda: req.POST[key], malnourished_form(key))


def assert_expr(truth, emsg):
    if not truth:
        raise ProperException(emsg)


def get_logged_in_user(req: HttpRequest):
    if LOGGED_IN_USER_KEY in req.session:
        return User.objects.get(pk=req.session[LOGGED_IN_USER_KEY])
    return None


def backend_command(command):
    def wrapper(*args, **kwargs):
        try:
            return command(*args, **kwargs)
        except ProperException as e:
            print(repr(e), e.response)
            return fail(e.response)
        except Exception as _:
            traceback.print_exc()
            return DEFAULT_FAIL_MESSAGE

    def dev_ui(template, data: Callable[[HttpRequest], dict] = lambda r: {}):
        return lambda req, **kwargs: render(req, f'devui/{template}.html', {**data(req), **kwargs})

    def service():
        return lambda req: JsonResponse(wrapper(req))

    def handler():
        return dev_ui('success', wrapper)

    wrapper.dev_ui = dev_ui
    wrapper.service = service
    wrapper.handler = handler

    return wrapper
