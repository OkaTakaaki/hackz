from django.contrib import admin
from .models import CustomUser
from .models import Collection

admin.site.register(CustomUser)
admin.site.register(Collection)
