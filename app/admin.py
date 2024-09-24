
from django.contrib import admin
from .models import AdminUser
from .models import Aphorism


admin.site.register(AdminUser)
admin.site.register(Aphorism)