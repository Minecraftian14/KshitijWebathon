import traceback

import re
from typing import Callable

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render


def fail(reason, data='null'):
    return {'status': 'fail', 'reason': reason, 'data': 'null'}


def success(reason, data='null'):
    return {'status': 'success', 'reason': reason, 'data': data}


default_fail_message = fail('server side exception based failure')


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


def backend_command(command):
    def wrapper(*args, **kwargs):
        try:
            return command(*args, **kwargs)
        except ProperException as e:
            print(repr(e.exception))
            return {'status': 'fail', 'reason': e.response, 'data': 'none'}
        except Exception as e:
            # print(repr(e))
            traceback.print_tb(e.__traceback__)
            return default_fail_message

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
