from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Путь к админке Django
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),  # Маршруты для приложения аккаунтов
    path('posts/', include('posts.urls')),  # Маршруты для приложения постов
    path('comments/', include('comments.urls')),  # Маршруты для приложения комментариев
    path('messages/', include('messaging.urls')),  # Маршруты для приложения сообщений
    path('moderation/', include('moderation.urls')),  # Маршруты для приложения модерации
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),  # Редирект на favicon
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Статические файлы для медиа

# Для режима отладки (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Статические файлы
