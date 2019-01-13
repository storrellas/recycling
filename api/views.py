from django.shortcuts import render

# Dependencies
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer


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
