from django.contrib import admin
from .models import CustomUser, Goal
from .models import Schedule

admin.site.register(CustomUser)
admin.site.register(Goal)
admin.site.register(Schedule)
