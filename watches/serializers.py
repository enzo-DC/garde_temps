from rest_framework import serializers
from .models import Brand, Complication, Watch


class BrandSerializer(serializers.ModelSerializer):
    """Serializer pour les marques"""
    watch_count = serializers.IntegerField(source='watches.count', read_only=True)
    
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country', 'founded_year', 'logo', 'description', 'watch_count']


class ComplicationSerializer(serializers.ModelSerializer):
    """Serializer pour les complications"""
    watch_count = serializers.IntegerField(source='watches.count', read_only=True)
    
    class Meta:
        model = Complication
        fields = ['id', 'name', 'description', 'watch_count']


class WatchListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des montres (vue catalogue)"""
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_country = serializers.CharField(source='brand.country', read_only=True)
    movement_display = serializers.CharField(source='get_movement_type_display', read_only=True)
    material_display = serializers.CharField(source='get_case_material_display', read_only=True)
    complication_count = serializers.IntegerField(source='complications.count', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Watch
        fields = [
            'id', 'model_name', 'reference_number', 'price', 'case_diameter',
            'movement_type', 'movement_display', 'case_material', 'material_display',
            'water_resistance', 'image', 'image_url', 'brand_name', 'brand_country', 
            'complication_count', 'created_at'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class WatchDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour une montre spécifique"""
    brand_obj = BrandSerializer(source='brand', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_country = serializers.CharField(source='brand.country', read_only=True)
    complications = ComplicationSerializer(many=True, read_only=True)
    movement_display = serializers.CharField(source='get_movement_type_display', read_only=True)
    material_display = serializers.CharField(source='get_case_material_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Watch
        fields = [
            'id', 'model_name', 'reference_number', 'price', 'case_diameter',
            'movement_type', 'movement_display', 'case_material', 'material_display',
            'water_resistance', 'description', 'image', 'image_url', 'serial_number',
            'brand', 'brand_name', 'brand_country', 'brand_obj', 'complications', 
            'created_at', 'updated_at'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
