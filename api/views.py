from django.shortcuts import render
from django.conf import settings
import operator

# Dependencies
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from geopy.distance import geodesic

# Project
from .serializers import *
from .models import *
from recycling import utils

logger = utils.get_logger()


class RecyclableMaterialViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    model = RecyclableMaterial
    queryset = RecyclableMaterial.objects.all()
    serializer_class = RecyclableMaterialSerializer
    renderer_classes = (JSONRenderer, )

class RecyclableSpotViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    model = RecyclableSpot
    queryset = RecyclableSpot.objects.all()
    serializer_class = RecyclableSpotSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=False, methods=['get'])
    def nearby(self, request, pk=None):

        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))

        # Get RecyclableSpot List
        recyclable_spot_queryset = RecyclableSpot.objects.all()


        # Calculate distance
        recyclable_spot_distance_list = {}
        for recyclable_spot in recyclable_spot_queryset:
            user_location = (user_latitude, user_longitude)
            spot_location = (recyclable_spot.latitude, recyclable_spot.longitude)
            recyclable_spot_distance_list[recyclable_spot.id] = geodesic(user_location, spot_location).kilometers

        # Get closest
        recyclable_spot_id_listed_sorted = sorted(recyclable_spot_distance_list.items(),
                                                    key=operator.itemgetter(1))
        recyclable_spot_closest_id_list = [i[0] for i in recyclable_spot_id_listed_sorted[0:settings.RECYCLABLE_SPOTS_LIMIT]]
        recyclable_spot_closest_queryset = recyclable_spot_queryset.filter(pk__in=recyclable_spot_closest_id_list)

        # Generate serializer
        serializer = RecyclableSpotDistanceSerializer(recyclable_spot_closest_queryset,
                                                      context={'distance_list': recyclable_spot_distance_list},
                                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MaterialViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    model = Material
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    renderer_classes = (JSONRenderer, )

class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=True, methods=['get'])
    def recyclablespot(self, request, pk=None):

        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))
        print(user_latitude)
        print(user_longitude)

        # Retrieve object
        product = self.get_object()

        # M.aterial set
        material_set = product.material_set.all()

        # Get Recyclable Spot
        recyclable_spot_list = []
        for material in material_set:
            spot_queryset = RecyclableSpot.objects.filter(recyclable_material=material.recyclable_material)
            spot_list = list(spot_queryset.values_list('id', flat=True))
            recyclable_spot_list.extend(spot_list)

        # Get RecyclableSpot List
        recyclable_spot_queryset = RecyclableSpot.objects.filter(pk__in=recyclable_spot_list)

        # Calculate distance
        recyclable_spot_distance_list = {}
        for recyclable_spot in recyclable_spot_queryset:
            user_location = (user_latitude, user_longitude)
            spot_location = (recyclable_spot.latitude, recyclable_spot.longitude)
            recyclable_spot_distance_list[recyclable_spot.id] = geodesic(user_location, spot_location).kilometers

        # Get closest
        recyclable_spot_id_listed_sorted = sorted(recyclable_spot_distance_list.items(),
                                                    key=operator.itemgetter(1))
        recyclable_spot_closest_id_list = [i[0] for i in recyclable_spot_id_listed_sorted[0:settings.RECYCLABLE_SPOTS_LIMIT]]
        recyclable_spot_closest_queryset = recyclable_spot_queryset.filter(pk__in=recyclable_spot_closest_id_list)

        # Generate serializer
        serializer = RecyclableSpotDistanceSerializer(recyclable_spot_closest_queryset,
                                                      context={'distance_list': recyclable_spot_distance_list},
                                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NewViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    model = New
    queryset = New.objects.all()
    serializer_class = NewSerializer
    renderer_classes = (JSONRenderer, )
