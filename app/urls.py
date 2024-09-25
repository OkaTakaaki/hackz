from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.generate_motivational_text, name='generate'),  # ホームページに対応するルート
]