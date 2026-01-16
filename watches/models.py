from django.db import models
from django.core.validators import MinValueValidator
import random
import string


class Brand(models.Model):
    """Marque de montres - Relation 1-N avec Watch"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la marque")
    country = models.CharField(max_length=100, verbose_name="Pays d'origine")
    founded_year = models.IntegerField(verbose_name="Année de fondation")
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name="Logo")
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Marque"
        verbose_name_plural = "Marques"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Complication(models.Model):
    """Complications horlogères - Relation N-N avec Watch"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    description = models.TextField(verbose_name="Description technique")
    
    class Meta:
        verbose_name = "Complication"
        verbose_name_plural = "Complications"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Watch(models.Model):
    """Modèle principal : Montre (7+ champs requis)"""
    
    MOVEMENT_CHOICES = [
        ('AUTO', 'Automatique'),
        ('MANUAL', 'Manuel'),
        ('QUARTZ', 'Quartz'),
        ('SOLAR', 'Solaire'),
    ]
    
    MATERIAL_CHOICES = [
        ('STEEL', 'Acier'),
        ('GOLD', 'Or'),
        ('TITANIUM', 'Titane'),
        ('CERAMIC', 'Céramique'),
        ('PLATINUM', 'Platine'),
        ('BRONZE', 'Bronze'),
    ]
    
    # Champs obligatoires (7 minimum selon les specs)
    model_name = models.CharField(max_length=200, verbose_name="Nom du modèle")
    reference_number = models.CharField(max_length=50, unique=True, verbose_name="Référence")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)], 
        verbose_name="Prix (€)"
    )
    case_diameter = models.IntegerField(
        validators=[MinValueValidator(20)], 
        verbose_name="Diamètre (mm)"
    )
    movement_type = models.CharField(
        max_length=10, 
        choices=MOVEMENT_CHOICES, 
        verbose_name="Type de mouvement"
    )
    case_material = models.CharField(
        max_length=10, 
        choices=MATERIAL_CHOICES, 
        verbose_name="Matériau du boîtier"
    )
    water_resistance = models.IntegerField(
        validators=[MinValueValidator(0)], 
        verbose_name="Étanchéité (m)"
    )
    description = models.TextField(verbose_name="Description / Histoire")
    
    # Champs supplémentaires
    image = models.ImageField(upload_to='watches/', blank=True, null=True, verbose_name="Photo")
    serial_number = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True, 
        null=True, 
        verbose_name="Numéro de série"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relations
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.CASCADE, 
        related_name='watches', 
        verbose_name="Marque"
    )
    complications = models.ManyToManyField(
        Complication, 
        blank=True, 
        related_name='watches', 
        verbose_name="Complications"
    )
    
    class Meta:
        verbose_name = "Montre"
        verbose_name_plural = "Montres"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand.name} {self.model_name} ({self.reference_number})"
    
    def save(self, *args, **kwargs):
        # Générer un numéro de série automatiquement si non fourni
        if not self.serial_number:
            self.serial_number = self.generate_serial_number()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_serial_number():
        """Génère un numéro de série unique"""
        while True:
            serial = 'SN-' + ''.join(random.choices(string.digits, k=8))
            if not Watch.objects.filter(serial_number=serial).exists():
                return serial
