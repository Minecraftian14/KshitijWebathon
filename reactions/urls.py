from django.urls import path

from .views import CSRFTokenView, index

app_name = 'reactions'
urlpatterns = [
    path('', index, name='index'),
    path('csrf_token/', CSRFTokenView.as_view(), name='csrf_token'),
]