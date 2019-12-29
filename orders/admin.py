from django.contrib import admin

from .models import PSAccount, Game


admin.site.register([PSAccount, Game])
