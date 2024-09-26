from django.contrib import admin
from .models import CustomUser, Goal, Schedule, Collection, AdminUser, Aphorism

admin.site.register(CustomUser)
admin.site.register(Goal)
admin.site.register(Schedule)
admin.site.register(Collection)
admin.site.register(AdminUser)
admin.site.register(Aphorism)