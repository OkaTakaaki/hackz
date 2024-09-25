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
    path('admin-login/', views.admin_login, name='admin_login'),  # ログインページ
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # ダッシュボード
    path('aphorism/<int:pk>/edit/', views.edit_aphorism, name='edit_aphorism'),  # 編集ページ
    path('aphorism/<int:pk>/delete/', views.delete_aphorism, name='delete_aphorism'),  # 削除ページ
    path('admin-logout/', views.admin_logout, name='admin_logout'),  # ログアウトページ
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
