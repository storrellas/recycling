# Dependencies
from rest_framework import serializers

# Project imports
from .models import *

class RecyclableMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclableMaterial
        fields = '__all__'

class RecyclableSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclableSpot
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    material_set = MaterialSerializer(required=False, many=True)
    class Meta:
        model = Product
        fields = '__all__'

class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = '__all__'

class RecyclableSpotDistanceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return self.context.get('distance_list')[obj.id]

    class Meta:
        model = RecyclableSpot
        fields = '__all__'
