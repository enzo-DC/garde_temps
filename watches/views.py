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
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


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
        """Génère un catalogue PDF standard (une page par montre)"""
        watch_ids = request.data.get('watch_ids', [])
        if not watch_ids:
            return Response({"error": "Aucun ID fourni"}, status=400)
        
        queryset = Watch.objects.filter(id__in=watch_ids).select_related('brand')
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        for i, watch in enumerate(queryset):
            if i > 0: p.showPage()
            p.setFont("Helvetica-Bold", 20)
            p.drawCentredString(width/2, height - 2*cm, "FICHE TECHNIQUE")
            p.setFont("Helvetica-Bold", 16)
            p.drawCentredString(width/2, height - 3.5*cm, f"{watch.brand.name} - {watch.model_name}")
            p.setStrokeColorRGB(0.77, 0.63, 0.35) # Gold
            p.line(2*cm, height - 4*cm, width - 2*cm, height - 4*cm)
            y = height - 5.5*cm
            data = [
                ("Référence", watch.reference_number),
                ("Prix", f"{watch.price} €"),
                ("Mouvement", watch.get_movement_type_display()),
                ("Matériau", watch.get_case_material_display()),
                ("Diamètre", f"{watch.case_diameter} mm"),
                ("Étanchéité", f"{watch.water_resistance} m"),
                ("Description", watch.description[:800] + "..."),
            ]
            for label, value in data:
                p.setFont("Helvetica-Bold", 11)
                p.drawString(2*cm, y, label)
                p.setFont("Helvetica", 11)
                if label == "Description":
                    y -= 0.6*cm
                    text_obj = p.beginText(2*cm, y)
                    text_obj.setFont("Helvetica", 10)
                    words = value.split()
                    line = ""
                    for word in words:
                        if len(line + word) < 90: line += word + " "
                        else:
                            text_obj.textLine(line)
                            line = word + " "
                            y -= 0.4*cm
                    text_obj.textLine(line)
                    p.drawText(text_obj)
                else:
                    p.drawString(6*cm, y, str(value))
                    y -= 0.8*cm
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    @action(detail=False, methods=['post'], url_path='export-wishlist')
    def export_wishlist(self, request):
        """Génère une liste condensée pour la wishlist"""
        watch_ids = request.data.get('watch_ids', [])
        queryset = list(Watch.objects.filter(id__in=watch_ids).select_related('brand'))
        total_price = sum(w.price for w in queryset)
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        p.setFont("Helvetica-Bold", 22)
        p.drawCentredString(width/2, height - 2*cm, "MA SÉLECTION EXCLUSIVE")
        
        p.setFont("Helvetica", 10)
        p.drawCentredString(width/2, height - 3*cm, "Catalogue personnalisé de garde-temps de prestige")
        
        # Summary bar
        p.setStrokeColorRGB(0.77, 0.63, 0.35)
        p.setFillColorRGB(0.98, 0.96, 0.92)
        p.rect(2*cm, height - 4.5*cm, width - 4*cm, 1*cm, fill=1)
        
        p.setFillColorRGB(0.2, 0.2, 0.2)
        p.setFont("Helvetica-Bold", 11)
        p.drawString(2.5*cm, height - 4*cm, f"COLLECTION : {len(queryset)} pièces")
        p.drawRightString(width - 2.5*cm, height - 4*cm, f"VALEUR TOTALE : {total_price} €")
        
        y = height - 6*cm
        for i, watch in enumerate(queryset):
            if y < 4*cm:
                p.showPage()
                y = height - 2*cm
            
            p.setStrokeColorRGB(0.77, 0.63, 0.35)
            p.setFillColorRGB(1, 1, 1) # Reset fill for next pages/items
            p.rect(2*cm, y - 3*cm, width - 4*cm, 3*cm)
            
            p.setFillColorRGB(0, 0, 0)
            p.setFont("Helvetica-Bold", 14)
            p.drawString(2.5*cm, y - 0.7*cm, f"{watch.brand.name} • {watch.model_name}")
            
            p.setFont("Helvetica", 10)
            p.drawString(2.5*cm, y - 1.5*cm, f"Réf: {watch.reference_number}")
            p.drawString(2.5*cm, y - 2.1*cm, f"Mouv: {watch.get_movement_type_display()}")
            p.drawString(9*cm, y - 2.1*cm, f"Matériau: {watch.get_case_material_display()}")
            
            p.setFont("Helvetica-Bold", 12)
            p.drawRightString(width - 2.5*cm, y - 1.5*cm, f"{watch.price} €")
            
            y -= 3.5*cm
            
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    @action(detail=False, methods=['post'], url_path='export-comparison')
    def export_comparison(self, request):
        """Génère un tableau comparatif"""
        watch_ids = request.data.get('watch_ids', [])
        queryset = list(Watch.objects.filter(id__in=watch_ids).select_related('brand'))
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(width/2, height - 2*cm, "COMPARATIF HAUTE HORLOGERIE")
        
        data = [
            ['Caractéristique'] + [f"{w.brand.name}\n{w.model_name}" for w in queryset],
            ['Prix'] + [f"{w.price} €" for w in queryset],
            ['Mouvement'] + [w.get_movement_type_display() for w in queryset],
            ['Boîtier'] + [w.get_case_material_display() for w in queryset],
            ['Diamètre'] + [f"{w.case_diameter} mm" for w in queryset],
            ['Étanchéité'] + [f"{w.water_resistance} m" for w in queryset],
        ]
        
        table = Table(data, colWidths=[3.5*cm] + [(width - 5.5*cm)/len(queryset)] * len(queryset))
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#c5a059")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor("#f9f9f9")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        table.wrapOn(p, width, height)
        table.drawOn(p, 1*cm, height - 10*cm)
        
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
