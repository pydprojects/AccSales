from django.contrib import admin

from .models import Roles, ExtendedUserData

admin.site.register([Roles, ExtendedUserData])
