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

# Serve media files:
# - Always in DEBUG
# - In production when not using S3 storage and MEDIA_URL is a relative path (starts with '/')
# This avoids relying on an environment flag and ensures covers upload work on Render with a mounted disk.
USE_S3 = getattr(settings, 'USE_S3', False)
if (settings.DEBUG or not USE_S3) and settings.MEDIA_URL.startswith('/'):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
