from django.contrib import admin
from .models import CustomUser
from .models import Collection
from .models import AdminUser
from .models import Aphorism

admin.site.register(CustomUser)
admin.site.register(Collection)
admin.site.register(AdminUser)
admin.site.register(Aphorism)