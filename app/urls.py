from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
]