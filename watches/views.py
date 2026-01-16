from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from .models import Brand, Complication, Watch
from .serializers import (
    BrandSerializer, 
    ComplicationSerializer, 
    WatchListSerializer, 
    WatchDetailSerializer
)
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


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

    @action(detail=False, methods=['post'], url_path='export-pdf')
    def export_pdf(self, request):
        """Génère un catalogue PDF pour une liste d'IDs reçue en POST"""
        watch_ids = request.data.get('watch_ids', [])
        if not watch_ids:
            return Response({"error": "Aucun ID de montre fourni"}, status=400)
        
        queryset = Watch.objects.filter(id__in=watch_ids).select_related('brand')
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        for i, watch in enumerate(queryset):
            if i > 0:
                p.showPage()
            
            p.setFont("Helvetica-Bold", 24)
            p.drawCentredString(width/2, height - 2*cm, "FICHE TECHNIQUE")
            
            p.setFont("Helvetica-Bold", 18)
            p.drawCentredString(width/2, height - 3*cm, f"{watch.brand.name} - {watch.model_name}")
            
            p.setStrokeColorRGB(0.8, 0.6, 0.2)
            p.line(2*cm, height - 3.5*cm, width - 2*cm, height - 3.5*cm)
            
            p.setFont("Helvetica-Bold", 12)
            y = height - 5*cm
            
            data = [
                ("Référence:", watch.reference_number),
                ("Prix:", f"{watch.price} €"),
                ("Mouvement:", watch.get_movement_type_display()),
                ("Matériau:", watch.get_case_material_display()),
                ("Diamètre:", f"{watch.case_diameter} mm"),
                ("Étanchéité:", f"{watch.water_resistance} m"),
                ("Description:", watch.description[:1000]),
            ]
            
            for label, value in data:
                p.setFont("Helvetica-Bold", 11)
                p.drawString(2*cm, y, label)
                p.setFont("Helvetica", 11)
                
                if label == "Description:":
                    y -= 0.6*cm
                    text_obj = p.beginText(2*cm, y)
                    text_obj.setFont("Helvetica", 10)
                    text_obj.setTextOrigin(2*cm, y)
                    words = value.split()
                    line = ""
                    for word in words:
                        if len(line + word) < 90:
                            line += word + " "
                        else:
                            text_obj.textLine(line)
                            line = word + " "
                            y -= 0.4*cm
                    text_obj.textLine(line)
                    p.drawText(text_obj)
                else:
                    p.drawString(6*cm, y, str(value))
                    y -= 0.8*cm
            
            p.setFont("Helvetica-Oblique", 8)
            p.drawCentredString(width/2, 1*cm, f"Chrono-Collections • Page {i+1}")
            
        p.save()
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="export_montres.pdf"'
        return response
