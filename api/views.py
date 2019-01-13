from django.shortcuts import render

# Dependencies
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



# Project
from .serializers import *
from .models import *
from recycling import utils

logger = utils.get_logger()


class RecyclableComponentViewSet(viewsets.ModelViewSet):

    model = RecyclableComponent
    queryset = RecyclableComponent.objects.all()
    serializer_class = RecyclableComponentSerializer
    renderer_classes = (JSONRenderer, )

class RecyclableSpotViewSet(viewsets.ModelViewSet):

    model = RecyclableSpot
    queryset = RecyclableSpot.objects.all()
    serializer_class = RecyclableSpotSerializer
    renderer_classes = (JSONRenderer, )

class ComponentViewSet(viewsets.ModelViewSet):

    model = Component
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    renderer_classes = (JSONRenderer, )

class ProductViewSet(viewsets.ModelViewSet):

    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=True, methods=['get'])
    def locatespot(self, request, pk=None):

        # Retrieve object
        product = self.get_object()

        # Component set
        component_set = product.component_set.all()

        # Get Recyclable Spot
        recyclable_spot_list = []
        for component in component_set:
            spot_queryset = RecyclableSpot.objects.filter(recyclable_component=component.recyclable_component)
            spot_list = list(spot_queryset.values_list('id', flat=True))
            recyclable_spot_list.extend(spot_list)

        print("-- Recyclable Spot List--")
        print(recyclable_spot_list)

        # Get RecyclableSpot List
        recyclable_spot_queryset = RecyclableSpot.objects.filter(pk__in=recyclable_spot_list)

        serializer = RecyclableSpotSerializer(recyclable_spot_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
