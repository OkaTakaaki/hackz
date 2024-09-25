from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('home', views.home, name='home'),
    path('goal', views.goal, name='goal'),
    path('input_goal/<int:year>/<int:month>/<int:day>/', views.detail_day, name='input_goal'),
    path('mycalendar/<int:year>/<int:month>/', views.MyCalendar.as_view(), name='mycalendar'),
    path('mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendarWithDate.as_view(), name='mycalendar_with_date'),  # 別のビューを使う
    path('plot/<int:year>/<int:month>/', views.plot, name='plot'),
]
