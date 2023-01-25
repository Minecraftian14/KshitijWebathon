from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Competition)
admin.site.register(models.TeamDetails)
