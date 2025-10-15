import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG or os.environ.get('DJANGO_SERVE_MEDIA', 'False') == 'True':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
