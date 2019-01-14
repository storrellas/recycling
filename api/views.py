from django.shortcuts import render

# Dependencies
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication



# Project
from .serializers import *
from .models import *
from recycling import utils

logger = utils.get_logger()


class RecyclableComponentViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    model = RecyclableComponent
    queryset = RecyclableComponent.objects.all()
    serializer_class = RecyclableComponentSerializer
    renderer_classes = (JSONRenderer, )

class RecyclableSpotViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    model = RecyclableSpot
    queryset = RecyclableSpot.objects.all()
    serializer_class = RecyclableSpotSerializer
    renderer_classes = (JSONRenderer, )

class ComponentViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    model = Component
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    renderer_classes = (JSONRenderer, )


from math import sin, cos, sqrt, atan2, radians
import operator
def calculate_distance(lat1, lon1, lat2, lon2):

    # approximate radius of earth in km
    R = 6373.0

    # local_lat1 = radians(52.2296756)
    # local_lon1 = radians(21.0122287)
    # local_lat2 = radians(52.406374)
    # local_lon2 = radians(16.9251681)

    local_lat1 = radians(lat1)
    local_lon1 = radians(lon1)
    local_lat2 = radians(lat2)
    local_lon2 = radians(lon2)

    dlon = local_lon2 - local_lon1
    dlat = local_lat2 - local_lat1

    a = sin(dlat / 2)**2 + cos(local_lat1) * cos(local_lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=True, methods=['get'])
    def locatespot(self, request, pk=None):

        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))
        print(user_latitude)
        print(user_longitude)

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

        # Get RecyclableSpot List
        recyclable_spot_queryset = RecyclableSpot.objects.filter(pk__in=recyclable_spot_list)

        # Calculate distance
        recyclable_spot_distance_list = {}
        for recyclable_spot in recyclable_spot_queryset:
            distance = calculate_distance(lat1=user_latitude, lon1=user_longitude,
                                          lat2=recyclable_spot.latitude, lon2=recyclable_spot.longitude)
            recyclable_spot_distance_list[recyclable_spot.id] = distance

        # Get closest
        recyclable_spot_id_listed_sorted = sorted(recyclable_spot_distance_list.items(),
                                                    key=operator.itemgetter(1))
        recyclable_spot_closest_id_list = [i[0] for i in recyclable_spot_id_listed_sorted[0:3]]
        recyclable_spot_closest_queryset = recyclable_spot_queryset.filter(pk__in=recyclable_spot_closest_id_list)

        # Generate serializer
        serializer = RecyclableSpotDistanceSerializer(recyclable_spot_closest_queryset,
                                                      context={'distance_list': recyclable_spot_distance_list},
                                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
