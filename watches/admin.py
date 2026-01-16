from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.utils.html import format_html
from .models import Brand, Complication, Watch
import json
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('dark_background') # Base style for all charts
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from django.core.serializers import serialize


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'founded_year', 'watch_count']
    list_filter = ['country']
    search_fields = ['name', 'country']
    
    def watch_count(self, obj):
        return obj.watches.count()
    watch_count.short_description = "Nombre de montres"


@admin.register(Complication)
class ComplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'watch_count']
    search_fields = ['name']
    
    def watch_count(self, obj):
        return obj.watches.count()
    watch_count.short_description = "Nombre de montres"


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = [
        'model_name', 'brand', 'reference_number', 'price', 
        'movement_type', 'case_diameter', 'pdf_button'
    ]
    list_filter = ['movement_type', 'case_material', 'brand']
    search_fields = ['model_name', 'reference_number', 'brand__name']
    filter_horizontal = ['complications']
    readonly_fields = ['serial_number', 'created_at', 'updated_at']
    
    actions = ['export_database_json', 'export_pdf_catalog', 'show_movement_chart', 'show_price_chart']
    
    def export_pdf_catalog(self, request, queryset):
        """Génère un catalogue PDF pour les montres sélectionnées"""
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        for i, watch in enumerate(queryset):
            if i > 0:
                p.showPage()
            
            # En-tête
            p.setFont("Helvetica-Bold", 24)
            p.drawCentredString(width/2, height - 2*cm, "FICHE TECHNIQUE")
            
            # Logo/Marque
            p.setFont("Helvetica-Bold", 18)
            p.drawCentredString(width/2, height - 3*cm, f"{watch.brand.name} - {watch.model_name}")
            
            p.setStrokeColorRGB(0.8, 0.6, 0.2)
            p.line(2*cm, height - 3.5*cm, width - 2*cm, height - 3.5*cm)
            
            # Contenu
            p.setFont("Helvetica-Bold", 12)
            y = height - 5*cm
            
            data = [
                ("Référence:", watch.reference_number),
                ("Prix:", f"{watch.price} €"),
                ("Mouvement:", watch.get_movement_type_display()),
                ("Matériau:", watch.get_case_material_display()),
                ("Diamètre:", f"{watch.case_diameter} mm"),
                ("Étanchéité:", f"{watch.water_resistance} m"),
                ("Description:", watch.description[:500] + "..." if len(watch.description) > 500 else watch.description),
            ]
            
            for label, value in data:
                p.setFont("Helvetica-Bold", 11)
                p.drawString(2*cm, y, label)
                p.setFont("Helvetica", 11)
                
                # Gestion du texte long (description)
                if label == "Description:":
                    y -= 0.6*cm
                    text_obj = p.beginText(2*cm, y)
                    text_obj.setFont("Helvetica", 10)
                    text_obj.setTextOrigin(2*cm, y)
                    # Simple wrap
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
            
            # Footer de page
            p.setFont("Helvetica-Oblique", 8)
            p.drawCentredString(width/2, 1*cm, f"Page {i+1} | Chrono-Collections • 2026")
            
        p.save()
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="catalogue_montres.pdf"'
        return response
    export_pdf_catalog.short_description = "📄 Générer un catalogue PDF (Sélection)"
    
    def pdf_button(self, obj):
        """Bouton pour générer le certificat PDF"""
        return format_html(
            '<a class="button" href="/admin/watches/watch/{}/certificate/" target="_blank">📄 Certificat PDF</a>',
            obj.pk
        )
    pdf_button.short_description = "Certificat"
    
    def get_urls(self):
        """Ajoute l'URL personnalisée pour le certificat PDF"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:watch_id>/certificate/', 
                self.admin_site.admin_view(self.generate_certificate), 
                name='watch_certificate'
            ),
        ]
        return custom_urls + urls
    
    def generate_certificate(self, request, watch_id):
        """Génère un PDF certificat d'authenticité avec ReportLab"""
        try:
            watch = Watch.objects.get(pk=watch_id)
        except Watch.DoesNotExist:
            return HttpResponse("Montre non trouvée", status=404)
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # En-tête élégant
        p.setFont("Helvetica-Bold", 28)
        p.drawCentredString(width/2, height - 3*cm, "CERTIFICAT D'AUTHENTICITÉ")
        
        # Sous-titre
        p.setFont("Helvetica-Oblique", 12)
        p.drawCentredString(width/2, height - 3.8*cm, "Garde-Temps de Prestige")
        
        # Ligne décorative dorée
        p.setStrokeColorRGB(0.8, 0.6, 0.2)
        p.setLineWidth(2)
        p.line(4*cm, height - 4.5*cm, width - 4*cm, height - 4.5*cm)
        
        # Informations de la montre
        p.setFont("Helvetica-Bold", 14)
        p.setFillColorRGB(0, 0, 0)
        y = height - 6.5*cm
        
        # Titre de section
        p.drawString(4*cm, y, "INFORMATIONS DU GARDE-TEMPS")
        y -= 1.2*cm
        
        # Détails
        p.setFont("Helvetica", 11)
        details = [
            ("Marque:", watch.brand.name),
            ("Modèle:", watch.model_name),
            ("Référence:", watch.reference_number),
            ("Numéro de série:", watch.serial_number or 'N/A'),
            ("", ""),  # Espace
            ("Mouvement:", watch.get_movement_type_display()),
            ("Matériau:", watch.get_case_material_display()),
            ("Diamètre du boîtier:", f"{watch.case_diameter} mm"),
            ("Étanchéité:", f"{watch.water_resistance} mètres"),
            ("", ""),  # Espace
            ("Prix catalogue:", f"{watch.price} €"),
        ]
        
        for label, value in details:
            if label:  # Si ce n'est pas un espace
                p.setFont("Helvetica-Bold", 11)
                p.drawString(4*cm, y, label)
                p.setFont("Helvetica", 11)
                p.drawString(9*cm, y, str(value))
            y -= 0.7*cm
        
        # Complications si présentes
        complications = watch.complications.all()
        if complications:
            y -= 0.5*cm
            p.setFont("Helvetica-Bold", 11)
            p.drawString(4*cm, y, "Complications:")
            y -= 0.7*cm
            p.setFont("Helvetica", 11)
            for comp in complications:
                p.drawString(5*cm, y, f"• {comp.name}")
                y -= 0.6*cm
        
        # Cadre décoratif
        p.setStrokeColorRGB(0.8, 0.6, 0.2)
        p.setLineWidth(1)
        p.rect(3*cm, 2*cm, width - 6*cm, height - 5*cm, stroke=1, fill=0)
        
        # Pied de page
        p.setFont("Helvetica-Oblique", 9)
        p.setFillColorRGB(0.5, 0.5, 0.5)
        p.drawCentredString(width/2, 1.5*cm, "Ce certificat atteste de l'authenticité du garde-temps décrit ci-dessus.")
        p.drawCentredString(width/2, 1*cm, "Chrono-Collections • 2026")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificat_{watch.reference_number}.pdf"'
        return response
    
    def export_database_json(self, request, queryset):
        """Exporte toute la base de données en JSON"""
        data = {
            'brands': json.loads(serialize('json', Brand.objects.all())),
            'complications': json.loads(serialize('json', Complication.objects.all())),
            'watches': json.loads(serialize('json', Watch.objects.all())),
        }
        
        response = JsonResponse(data, safe=False, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = 'attachment; filename="database_export.json"'
        return response
    export_database_json.short_description = "📦 Exporter la BDD en JSON"

    def _get_movement_chart_base64(self):
        """Helper pour générer le graphique mouvement en base64"""
        movements = Watch.objects.values_list('movement_type', flat=True)
        movement_counts = {}
        for m in movements:
            movement_counts[m] = movement_counts.get(m, 0) + 1
        
        if not movement_counts:
            return None
        
        labels = [dict(Watch.MOVEMENT_CHOICES).get(k, k) for k in movement_counts.keys()]
        sizes = list(movement_counts.values())
        # Palette Luxe: Or, Argent, Platine, Bronze
        colors = ['#c5a059', '#a6a6a6', '#e5e4e2', '#cd7f32']
        
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('none') # Fond transparent
        ax.set_facecolor('none')
        
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%', 
            startangle=90, colors=colors,
            pctdistance=0.85, explode=[0.05]*len(sizes)
        )
        
        # Donut effect
        centre_circle = plt.Circle((0,0), 0.70, fc='#121212')
        fig.gca().add_artist(centre_circle)
        
        plt.setp(autotexts, size=8, weight="bold", color="black")
        plt.setp(texts, size=10, color="#c5a059")
        
        plt.title('DISTRIBUTION DES MOUVEMENTS', color='#c5a059', fontsize=12, fontweight='bold', pad=20)
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True, dpi=100)
        plt.close(fig)
        return base64.b64encode(buffer.getvalue()).decode()

    def _get_price_chart_base64(self):
        """Helper pour générer le graphique prix moyen en base64"""
        from django.db.models import Avg
        brand_prices = Brand.objects.annotate(
            avg_price=Avg('watches__price')
        ).filter(avg_price__isnull=False).order_by('-avg_price')[:5] # Top 5
        
        if not brand_prices:
            return None
        
        brands = [b.name for b in brand_prices]
        prices = [float(b.avg_price) for b in brand_prices]
        
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        
        bars = ax.bar(brands, prices, color='#c5a059', alpha=0.8, edgecolor='#a6a6a6')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 500,
                    f'{int(height)}€', ha='center', va='bottom', color='#a6a6a6', fontsize=8)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#333')
        ax.spines['bottom'].set_color('#333')
        ax.tick_params(colors='#a6a6a6', labelsize=8)
        
        plt.title('PRIX MOYEN PAR MARQUE', color='#c5a059', fontsize=12, fontweight='bold', pad=20)
        
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True, dpi=100)
        plt.close(fig)
        return base64.b64encode(buffer.getvalue()).decode()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['movement_chart'] = self._get_movement_chart_base64()
        extra_context['price_chart'] = self._get_price_chart_base64()
        return super().changelist_view(request, extra_context=extra_context)
    
    def show_movement_chart(self, request, queryset):
        """Action pour afficher le graphique mouvement (version isolée)"""
        chart_base64 = self._get_movement_chart_base64()
        if not chart_base64:
            return HttpResponse("Désolé, aucune donnée pour générer le graphique.")
        return HttpResponse(base64.b64decode(chart_base64), content_type='image/png')
    show_movement_chart.short_description = "📊 Graphique: Répartition Mouvements"
    
    def show_price_chart(self, request, queryset):
        """Action pour afficher le graphique prix (version isolée)"""
        chart_base64 = self._get_price_chart_base64()
        if not chart_base64:
            return HttpResponse("Désolé, aucune donnée pour générer le graphique.")
        return HttpResponse(base64.b64decode(chart_base64), content_type='image/png')
    show_price_chart.short_description = "📊 Graphique: Prix Moyen par Marque"
