from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ViewCollectionList

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('home', views.home, name='home'),
    path('collections', ViewCollectionList.as_view(), name='collection-list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)