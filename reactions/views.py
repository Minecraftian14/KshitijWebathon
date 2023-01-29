from django.views import View
from django.http import JsonResponse
from django.middleware.csrf import get_token


class CSRFTokenView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'csrf_token': get_token(request)})
