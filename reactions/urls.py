from django.urls import path

from .views import CSRFTokenView

app_name = 'reactions'
urlpatterns = [
    path('csrf_token/', CSRFTokenView.as_view(), name='csrf_token'),
]