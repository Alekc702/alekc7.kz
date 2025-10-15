import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Serve media files:
# - Always in DEBUG
# - In production when not using S3 storage and MEDIA_URL is a relative path (starts with '/')
# This avoids relying on an environment flag and ensures covers upload work on Render with a mounted disk.
USE_S3 = getattr(settings, 'USE_S3', False)
if (settings.DEBUG or not USE_S3) and settings.MEDIA_URL.startswith('/'):
    # Add explicit media route first to avoid any routing precedence issues
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT }),
    ]
    # Also keep the helper for consistency (no-op if above already matches)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# App routes come after media to ensure media takes precedence
urlpatterns += [
    path('', include('games.urls')),
    path('users/', include('users.urls')),
]
