from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Brand, Complication, Watch
from .serializers import (
    BrandSerializer, 
    ComplicationSerializer, 
    WatchListSerializer, 
    WatchDetailSerializer
)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API en lecture seule pour les marques
    Filtres: recherche par nom et pays
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name', 'founded_year']
    ordering = ['name']


class ComplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API en lecture seule pour les complications
    Filtres: recherche par nom
    """
    queryset = Complication.objects.all()
    serializer_class = ComplicationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class WatchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API en lecture seule pour les montres
    Filtres disponibles:
    - movement_type: Type de mouvement (AUTO, MANUAL, QUARTZ, SOLAR)
    - case_material: Matériau (STEEL, GOLD, TITANIUM, etc.)
    - brand: ID de la marque
    - complications: ID de complication
    - brand__country: Pays de la marque (ex: Suisse, Japon)
    - case_diameter__lte: Diamètre max (ex: 40 pour "moins de 40mm")
    - price__lte: Prix maximum
    - price__gte: Prix minimum
    """
    queryset = Watch.objects.select_related('brand').prefetch_related('complications')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['model_name', 'reference_number', 'brand__name', 'description']
    filterset_fields = {
        'movement_type': ['exact'],
        'case_material': ['exact'],
        'brand': ['exact'],
        'brand__country': ['exact', 'icontains'],
        'complications': ['exact'],
        'case_diameter': ['exact', 'lte', 'gte'],
        'price': ['exact', 'lte', 'gte'],
        'water_resistance': ['exact', 'lte', 'gte'],
    }
    ordering_fields = ['price', 'case_diameter', 'created_at', 'model_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Utilise le serializer détaillé pour la vue de détail"""
        if self.action == 'retrieve':
            return WatchDetailSerializer
        return WatchListSerializer
