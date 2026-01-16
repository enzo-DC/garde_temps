"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from watches.views import BrandViewSet, ComplicationViewSet, WatchViewSet

# Configuration du router DRF
router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'complications', ComplicationViewSet, basename='complication')
router.register(r'watches', WatchViewSet, basename='watch')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Interface de login DRF
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personnalisation de l'admin
admin.site.site_header = "Garde-Temps Administration"
admin.site.site_title = "Chrono-Collections"
admin.site.index_title = "Gestion des Montres de Luxe"
