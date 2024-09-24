# urls.py
from django.conf import settings
from django.conf.urls.static import static
# urls.py
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),  # ログインページ
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # ダッシュボード
    path('aphorism/<int:pk>/edit/', views.edit_aphorism, name='edit_aphorism'),  # 編集ページ
    path('aphorism/<int:pk>/delete/', views.delete_aphorism, name='delete_aphorism'),  # 削除ページ
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
