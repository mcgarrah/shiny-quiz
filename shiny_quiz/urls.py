"""
URL configuration for shiny_quiz project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Remove allauth_ui.urls as it doesn't exist - the package provides templates only
    path('accounts/', include('allauth.urls')),     # Standard allauth URLs
    path('accounts/', include('accounts.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('quiz/', include('quiz.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)