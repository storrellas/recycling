# Dependencies
from rest_framework import serializers

# Project imports
from .models import *

class RecyclableComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclableComponent
        fields = '__all__'

class RecyclableSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclableSpot
        fields = '__all__'

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RecyclableSpotDistanceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return self.context.get('distance_list')[obj.id]

    class Meta:
        model = RecyclableSpot
        fields = '__all__'
